from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import dateutil.parser

app = Flask(__name__)

# MongoDB Local Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['techstax_assignment']
collection = db['github_events']

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    event_doc = None

    if event_type == 'push':
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        timestamp = datetime.utcnow()
        msg = f'"{author}" pushed to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
        event_doc = { "type": "PUSH", "author": author, "to_branch": to_branch, "timestamp": timestamp, "message": msg }

    elif event_type == 'pull_request':
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp = datetime.utcnow()
        action = data['action']

        if action == 'closed' and data['pull_request']['merged'] is True:
            msg = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
            event_doc = { "type": "MERGE", "author": author, "from_branch": from_branch, "to_branch": to_branch, "timestamp": timestamp, "message": msg }
        elif action == 'opened':
            msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
            event_doc = { "type": "PULL_REQUEST", "author": author, "from_branch": from_branch, "to_branch": to_branch, "timestamp": timestamp, "message": msg }

    if event_doc:
        collection.insert_one(event_doc)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "ignored"}), 200

@app.route('/api/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10))
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=5000)