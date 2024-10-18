
# ChatGPT Meta Messaging

This project integrates OpenAI's GPT assistant ([OpenAI Assistant](https://platform.openai.com/docs/assistants/overview)) with Meta messaging platforms (e.g., Instagram, Facebook) to provide automated messaging solutions. This is particularly useful for automated support chat or engagement ads with messaging as a conversion event.

## Features
- Integration with Meta's Instagram and Facebook messaging APIs.
- Automated response generation using OpenAI's GPT assistant API.
- Dockerized for easy deployment.
- Hosted on Google Cloud Run.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Build and Deployment](#build-and-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support and Donations](#support-and-donations)

---

## Installation

### Prerequisites
- [Docker](https://www.docker.com/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- A Meta App to access Instagram and Facebook APIs ([Meta Developer Documentation](https://developers.facebook.com/docs/development))
- For Instagram messaging, apply for `instagram_manage_messages` advanced access to allow the bot to send messages to Instagram. (Not needed for Facebook pages, where standard access is sufficient.)

### Steps to Launch the Script on Google Cloud Functions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatgpt-meta-messaging.git
   ```
2. Update the Dockerfile with the necessary keys and environment variables.
3. Build the Docker image:
   ```bash
   docker buildx build --platform linux/amd64 -t my-backend-app .
   ```
4. Push the Docker image to Google Artifact Registry.
5. Deploy the image as a Google Cloud Function.

### Usage
1. Copy the Google Cloud Function (GCF) URL and paste it into the Meta App dashboard under the Webhook field.
2. In the Webhooks section, select the Page product from the dropdown and subscribe only for messages. Then, select Instagram and again subscribe only for messages.
3. Do not subscribe separately for Messenger and Instagram products—Webhooks is enough to handle both.

### Steps to Set Up a Meta App
1. Create a Meta App.
2. Add `page_manage_messaging` (basic-level permission) and `instagram_manage_messaging` (basic-level permission).
3. Create a test app to unblock `instagram_basic` permission.
4. Apply for `instagram_manage_messages` advanced-level permission.
5. Use an Instagram account where you can provide login credentials to Meta testers (often based in the Philippines), ensuring that Meta security measures (e.g., two-factor authentication) will not block the testers' access.
6. Use the following template for the required Meta application text:

#### Platform Settings
- **Platform:** Desktop  
- **Site URL:** [URL to Google Cloud Function]  
- **App Description:**  
  This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. It requires advanced-level access to the `instagram_manage_messages` permission in order to reply to any user who sends a direct message to the Instagram account.  
  You can send direct messages to `@[IG_account]` to test the functionality. Here are the relevant details:  
  [Provide login and password]

#### instagram_manage_messages Permission Request
- **Use Case:**  
  This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. It requires advanced-level access to the `instagram_manage_messages` permission in order to reply to any user who sends a direct message to the Instagram account.

#### instagram_basic Permission Request
- **Use Case:**  
  This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. In order to gain advanced-level access to the `instagram_manage_messages` permission, we also need access to `instagram_basic`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support and Donations
If you find this project helpful and would like to support its development, you can make a donation:
