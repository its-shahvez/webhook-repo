# GitHub Webhook Event Receiver

This project is a Flask-based application that listens to GitHub Webhooks (Push, Pull Request, Merge) and stores the event data in MongoDB. It also features a real-time UI that updates every 15 seconds.

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Database:** MongoDB
- **Frontend:** HTML, JavaScript (Polling)
- **Tools:** Ngrok (for local tunneling)

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone [https://github.com/its-shahvez/webhook-repo.git](https://github.com/its-shahvez/webhook-repo.git)
   cd webhook-repo
   Install Dependencies

Bash
pip install -r requirements.txt
Start MongoDB Make sure your MongoDB service is running locally on port 27017.

Run the Application

Bash
python app.py
The app will run at http://localhost:5000.

Setup Webhook

Use Ngrok to expose port 5000: ngrok http 5000

Add the generated URL to your GitHub Repository Webhook settings (/webhook endpoint).

Select application/json as content type.

✅ Features
Handles PUSH events.

Handles PULL_REQUEST events.

Handles MERGE events (Brownie Point Logic included).

Displays events in a clean UI with auto-refresh.

Author: Mohd Shahvez
