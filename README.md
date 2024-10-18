# ChatGPT Meta Messaging

This project integrates OpenAI's GPT assistant (https://platform.openai.com/docs/assistants/overview) with Meta messaging platforms (e.g., Instagram, Facebook) to provide automated messaging solutions. The solution is useful particularly for automated support chat and for engagement ads with messaging as conversion event.

## Features
- Integration with Meta's Instagram and Facebook messaging APIs.
- Automated response generation using OpenAI's GPT assistant api.
- Dockerized for easy deployment.
- Google cloud run for hosting.

## Table of Contents
- [Prerequisites](#Prerequisites)
- [Steps-to-launch-the-script-on-GCF](#Steps-to-launch-the-script-on-GCF)
- [Usage](#Usage)
- [Steps-to-setup-META-App](#Steps-to-setup-META-App)
- [License](#license)
- [Support and Donations](#support-and-donations)

---

## Prerequisites
- [Docker](https://www.docker.com/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- A Meta App to access Instagram and Facebook APIs (https://developers.facebook.com/docs/development)
- For instagram messaging apply for instagram_manage_messages advanced access in order for bot to be able to send messages to instagram (Not needed to facebook pages), With Facebook you are good to go with standard access.

## Steps-to-launch-the-script-on-GCF
1. Clone the repository:
   git clone https://github.com/yourusername/chatgpt-meta-messaging.git
2. Fulfil Docker file Keys and other variables
3. Dockerise 
   docker buildx build --platform linux/amd64 -t my-backend-app .
4. Push to Google Artifact Repository
5. Create google function from Docker

## Usage
1. Copy GCF url and paste it in meta app dashboard webhook field
2. In webhook product choose page from drop down and subscribe just for message, then choose instagram and again subscribe just for messages
3. Do not subscribe for separate products Messager and Instagram as Webhooks is enough for this

## Steps-to-setup-META-App
1. Create App
2. Add `page_manage_messaging` basic level permission, add `instagram_manage_messaging` basic permission
3. Create test App in order to unblock instagram_basic permission
4. Apply for `instagram_manage_messages` advance level permission
5. Use an Instagram account where you can provide login credentials to Meta testers (often based in the Philippines), ensuring that Meta security measures (e.g., two-factor authentication) will not block the testers' access.
6. Use text as follows as an example:

   #Platform Settings
   Desktop
   Site URL: `[url to GCF]`
   This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. It requires advanced-level access to the instagram_manage_messages permission in order to reply to any user who sends a direct message to the Instagram account.

   You can send direct messages to `@[IG_account]` in order to test the functionality. Here are the relevant details:
   [Provide login and password]

   #instagram_manage_messages
   #Tell us how you're using this permission or feature
   This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. It requires advanced-level access to the instagram_manage_messages permission in order to reply to any user who sends a direct message to the Instagram account.

   #instagram_basic
   #Tell us how you're using this permission or feature
   This app is a server-to-server application—a chatbot that replies to direct messages on an associated Instagram account. It requires advanced-level access to the instagram_manage_messages permission in order to reply to any user who sends a direct message to the Instagram account. In order to get advanced-level access to the instagram_manage_messages permission I also need access to instagram_basic.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Support and Donations
If you find this project helpful and would like to support its development, you can make a donation:
- https://www.paypal.com/paypalme/kdylko/