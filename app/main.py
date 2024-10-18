import functions_framework
import os
import time
from flask import Flask, request
from openai import OpenAI
import requests
import re

# Set up your OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Set up other environment variables
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')
INSTAGRAM_GRAPH_API_URL = os.getenv('INSTAGRAM_GRAPH_API_URL', 'https://graph.facebook.com/v20.0')

# In-memory storage for thread_id to sender_id mapping
sender_thread_map = {}
meta_to_openai_message_map = {}
processed_message_ids = set()

# Create Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook_handler():
    """Webhook HTTP Cloud Function with OpenAI Assistant integration.
    Args:
        request (flask.Request): The request object.
    Returns:
        A response confirming the webhook request has been processed.
    """
    # Handle verification challenge from Facebook Messenger
    try:
        if request.method == 'GET':
            verify_token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')

            if verify_token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return 'Invalid verification token', 403

        elif request.method == 'POST':
            request_json = request.get_json(silent=True)
            if request_json:
                entries = request_json.get('entry')
                if isinstance(entries, list) and len(entries) > 0:
                    messaging = entries[0].get('messaging')
                    if isinstance(messaging, list) and len(messaging) > 0:
                        message = messaging[0].get('message')
                        
                        if 'read' in message:
                            return  "Read event detected, skipping...", 200 # Skip processing if it's a read event
                        
                        # Handle unsend requests (is_deleted = True)
                        if 'is_deleted' in message and message['is_deleted']:
                            sender_id = messaging[0]['sender']['id']
                            message_id = message['mid']
                            print(f"Unsend request detected for message ID: {message_id}")
                            remove_message_from_thread(sender_id, message_id)
                            return "Message unsend request handled", 200


                        if message and not message.get('is_echo'):
                            response_message = process_incoming_message(request_json)
                            print("Response message generated: %s", response_message)
                            return response_message, 200
            return 'No reply needed', 200
    except Exception as e:
        print("Error processing request: %s", str(e))
        return 'Internal Server Error', 500

def process_incoming_message(data):
    """Processes incoming message and sends it to OpenAI Assistant for a response."""
    messages = data['entry'][0]['messaging'][0]['message']['text']
    meta_message_id = data['entry'][0]['messaging'][0]['message']['mid']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']

    if meta_message_id in processed_message_ids:
        print(f"Message {meta_message_id} already processed. Skipping...")
        return "Duplicate message"

    # Add the message ID to the set
    processed_message_ids.add(meta_message_id)

    # Check if we already have a thread for this sender
    if sender_id in sender_thread_map:
        thread_id = sender_thread_map[sender_id]
        print("Using existing thread ID:", thread_id)
    else:
        # Create a new thread and save it in the map
        thread = client.beta.threads.create()
        thread_id = thread.id
        sender_thread_map[sender_id] = thread_id
        print("Created new thread ID:", thread_id, "for sender ID:", sender_id)

    # Add message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=messages
    )

    # Store the mapping of Meta message ID to OpenAI message ID
    meta_to_openai_message_map[meta_message_id] = message.id
    print(f"Mapped Meta message ID {meta_message_id} to OpenAI message ID {message.id}")
    
    
    # Create run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )
    
    # Wait for completion
    wait_on_run(run, thread_id)
    print("Run status: ",run.status)
    print("Run details: ",run)


    # Collect response
    if run.status == "completed":
        ai_response = client.beta.threads.messages.list(thread_id=thread_id)
        print(ai_response)
        for message in ai_response:
            if message.role == 'assistant':
                assert message.content[0].type == "text"
                print(message.content[0].text.value)
                ai_text_response = message.content[0].text.value
                send_message_instagram(ai_text_response, sender_id)
                break

    
    return ai_text_response

def remove_message_from_thread(sender_id, meta_message_id):
    """Removes all messages associated with a given Meta message ID from the OpenAI thread when an unsend request is detected."""
    if sender_id in sender_thread_map:
        thread_id = sender_thread_map[sender_id]
        
        # Look up the OpenAI message IDs associated with the Meta message ID
        if meta_message_id in meta_to_openai_message_map:
            openai_message_ids = meta_to_openai_message_map[meta_message_id]  # Assuming this is a list if multiple messages are mapped
            
            # Ensure we handle one or multiple OpenAI message IDs
            if not isinstance(openai_message_ids, list):
                openai_message_ids = [openai_message_ids]
            
            # Iterate through all OpenAI message IDs and remove each from the thread
            for openai_message_id in openai_message_ids:
                try:
                    # Delete the message from the OpenAI thread
                    client.beta.threads.messages.delete(thread_id=thread_id, message_id=openai_message_id)
                    print(f"Message {meta_message_id} (OpenAI ID: {openai_message_id}) removed from thread {thread_id}")
                except Exception as e:
                    print(f"Error removing message {openai_message_id} from thread {thread_id}: {str(e)}")
            
            # Optionally, remove the mapping after deletion
            del meta_to_openai_message_map[meta_message_id]
        else:
            print(f"No OpenAI message found for Meta message ID {meta_message_id}")
    else:
        print(f"No thread found for sender {sender_id}")

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def send_message_instagram(message_text, recipient_id):
    url = f"{INSTAGRAM_GRAPH_API_URL}/{PAGE_ID}/messages"
    
    message_text = clean_text(message_text)

    headers = {
        "Content-Type": "application/json",
    }
    params = {
        "access_token": ACCESS_TOKEN,
    }

    # Split the message_text into batches if it exceeds 1000 characters
    batch_size = 1000
    batches = [message_text[i:i + batch_size] for i in range(0, len(message_text), batch_size)]

    for batch in batches:
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": batch},
            "messaging_type": "RESPONSE",
        }

        response = requests.post(url, headers=headers, json=data, params=params)

        if response.status_code == 200:
            print("Batch sent successfully!")
        else:
            print(f"Failed to send batch: {response.status_code}, {response.text}")

    return

def clean_text(text):
    # Remove double asterisks (bold)
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    
    # Remove [source] pattern (e.g.,  )
    cleaned_text = re.sub(r'【.*?†source】', '', cleaned_text)

    # Remove ### patterns (headings or other similar patterns)
    cleaned_text = re.sub(r'###\s*', '', cleaned_text)
    
    # Optionally, remove extra spaces if needed
    cleaned_text is cleaned_text.strip()

    return cleaned_text

# Ensure the application listens on the correct port when deployed
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
