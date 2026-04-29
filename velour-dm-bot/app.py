from flask import Flask, request
import requests
import os
import json
from dotenv import load_dotenv
from responses import get_response

load_dotenv()

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_ACCOUNT_ID = os.getenv("IG_ACCOUNT_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    
    print("\n=== WEBHOOK RECEIVED ===")
    print(json.dumps(data, indent=2))
    
    try:
        # Check for Instagram webhook format
        if data.get("object") == "instagram":
            for entry in data.get("entry", []):
                # Look for messaging array
                if "messaging" in entry:
                    for messaging in entry["messaging"]:
                        sender_id = messaging.get("sender", {}).get("id")
                        message = messaging.get("message", {})
                        message_text = message.get("text")
                        
                        if message_text and not message.get("is_echo"):
                            print(f"\n>>> Message from {sender_id}: {message_text}")
                            reply_text = get_response(message_text)
                            print(f"<<< Reply: {reply_text}")
                            
                            # Send reply using Facebook Page Messenger endpoint

                            # Send reply using Instagram endpoint
                            url = f"https://graph.facebook.com/v25.0/{IG_ACCOUNT_ID}/messages"
                            payload = {
                                "recipient": {"id": sender_id},
                                "message": {"text": reply_text},
                                "access_token": ACCESS_TOKEN
                            }
 
                            print(f"\n>>> Sending to {sender_id}: {reply_text}")
                            response = requests.post(url, json=payload)
                            print(f"Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)