# 🚀 GroupMe Chatbot

## 📌 Overview

A powerful chatbot for GroupMe, built using **FastAPI** (backend) and **Next.js** (frontend). This bot streamlines group messaging by requiring admin approval before forwarding messages and integrates with an **LLM (Large Language Model)** for content moderation and improvement.

## ✨ Features

✅ **Seamless Group Messaging** - Send messages to GroupMe groups effortlessly.  
✅ **Admin Approval System** - Messages require admin validation before being forwarded.  
✅ **Multi-Group Forwarding** - Once approved, messages are sent to multiple groups.  
✅ **AI-Powered Message Enhancement** - Utilizes LLM to refine messages before sending.  
✅ **Secure & Scalable** - Built with MongoDB for reliable data management.

## 🛠️ Technologies Used

- **Backend:** FastAPI  
- **Frontend:** Next.js  
- **Database:** MongoDB  
- **Deployment:** Render  
- **Messaging API:** GroupMe API

## 🚀 Installation & Setup

### ✅ Prerequisites
- Python 3.11+
- FastAPI
- Uvicorn
- Requests (for GroupMe API)
- Node.js & npm (for frontend)
- MongoDB

### 📂 Steps to Run Locally

1️⃣ **Clone the Repository**
```bash
git clone https://github.com/1atharvad/groupme-bot-master.git
cd groupme-bot-master
```

2️⃣ **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

3️⃣ **Install Frontend Dependencies**
```bash
cd frontend
npm install
```

4️⃣ **Set Up Environment Variables**
```plaintext
CALLBACK_URL=URL after GroupMe auth successful
DB_NAME=MongoDB database name
FASTAPI_ENV=development
MODEL=Perplexity model name
MONGO_URI=MongoDB URI
NEXT_PUBLIC_API_URL=FastAPI hosted API URL
PERPLEXITY_API_TOKEN=API token for Perplexity
PRIVATE_KEY=MongoDB private key
PROJECT_ID=MongoDB project ID
PUBLIC_KEY=MongoDB public key
GROUPME_BOT_ID=Your GroupMe bot ID
GROUPME_ACCESS_TOKEN=Your GroupMe API token
ADMIN_USER_IDS=Comma-separated list of admin user IDs
```

5️⃣ **Run the Backend Locally**
```bash
npm run dev
```

6️⃣ **Run the Frontend Locally**
```bash
cd frontend
npm run dev  # or yarn dev
```

## 🌐 API Endpoints

| Method  | Endpoint                       | Description                                     |
|---------|--------------------------------|------------------------------------------------|
| GET     | `/api/get-client-id/{username}`  | Get client ID for the username                 |
| POST    | `/api/set-client-id`            | Set client ID for username                     |
| GET     | `/api/get-group-ids/{username}`  | Get all group IDs where user is a member       |
| GET     | `/api/get-bot-groups/{username}` | Get details of all bots created by the user    |
| POST    | `/api/set-bot-groups`           | Create a bot                                   |
| PUT     | `/api/update-bot-groups/{id}`   | Update an existing bot created by user        |
| DELETE  | `/api/delete-bot-group/{id}`    | Delete a bot created by user                   |

## 🚀 Deployment

This chatbot is **deployed on Render**.

🔗 **Live URL:** [GroupMe Bot](https://groupme-bot-master.onrender.com/)

## 💬 Chatbot Commands

🤖 **GroupMe Chatbot Commands** 🤖

✅ `/help` - Show available commands  
✅ `/need_approval <message_text>` - Sends the message for approval  
✅ `/improve <message_text>` - Enhances message using AI  
✅ `/improve` - Enhances the previous message using AI  
✅ `/cancel` - Cancels the current message thread  
✅ `/need_approval` - Sends the previous message for approval  
✅ `/approve` - Admin approves the message for forwarding  
✅ `/reject` - Rejects the message (no further action)  
✅ `/status` - Check bot status  

## 📜 License

**MIT License** - Feel free to use and modify!

## 📩 Contact
For issues, suggestions, or contributions, reach out to **Atharva D**. 🚀
