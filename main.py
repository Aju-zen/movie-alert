from flask import Flask, request, render_template
import json
import os
import requests

app = Flask(__name__)

BOT_TOKEN = "8239634152:AAHB23IElJeo5xx9pSHTmdAMiI_DZiOHQbc"
SUBSCRIBERS_FILE = 'subscribers.json'

if not os.path.exists(SUBSCRIBERS_FILE):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    movie = request.form['movie'].strip()
    city = request.form['city'].strip()
    telegram_username = request.form['telegram_username'].strip()

    if movie and city and telegram_username:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            subscribers = json.load(f)

        new_sub = {
            "movie": movie,
            "city": city,
            "telegram_username": telegram_username
        }

        if new_sub not in subscribers:
            subscribers.append(new_sub)
            with open(SUBSCRIBERS_FILE, 'w') as f:
                json.dump(subscribers, f, indent=2)

    return render_template('success.html')

@app.route('/test-alert', methods=['POST'])
def test_alert():
    telegram_username = request.form['telegram_username'].strip()
    message = "✅ This is a test alert from @alertsbyzen_bot.\n\nYou're subscribed for movie alerts."

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": f"@{telegram_username}",
            "text": message
        }
        requests.post(url, data=payload)
        return "Test alert sent!"
    except Exception as e:
        return f"Failed to send test alert: {e}"

