from flask import Flask, request, render_template_string, jsonify
import json
import os

app = Flask(__name__)

# Create subscribers.json if it doesn't exist
if not os.path.exists('subscribers.json'):
    with open('subscribers.json', 'w') as f:
        json.dump([], f)

# HTML template for the main page
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Movie Alert Subscription</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 36px;
        }
        input, button {
            padding: 12px;
            margin: 10px;
            font-size: 16px;
        }
        #subscribe-btn {
            background-color: #00ff88;
            border: none;
            cursor: pointer;
        }
        #test-btn {
            background-color: #ff0080;
            border: none;
            cursor: pointer;
            color: white;
        }
    </style>
</head>
<body>
    <h1>🎬 BookMyShow Movie Alert</h1>
    <p>Subscribe to get alerts when your movie is available!</p>
    <form id="subscribe-form">
        <input type="text" id="movie" placeholder="Movie name" required />
        <input type="text" id="location" placeholder="Location" required />
        <input type="text" id="chat_id" placeholder="Your Telegram Chat ID" required />
        <br>
        <button id="subscribe-btn" type="submit">Subscribe</button>
        <button id="test-btn" type="button" onclick="testAlert()">Send Test Alert</button>
    </form>

    <script>
        const form = document.getElementById('subscribe-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const movie = document.getElementById('movie').value;
            const location = document.getElementById('location').value;
            const chat_id = document.getElementById('chat_id').value;

            const res = await fetch('/subscribe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ movie, location, chat_id })
            });

            const data = await res.json();
            alert(data.status === 'success' ? '✅ Subscribed!' : '❌ Failed to subscribe');
        });

        async function testAlert() {
            const chat_id = document.getElementById('chat_id').value;
            if (!chat_id) {
                alert('Please enter your chat ID to test alert');
                return;
            }

            const res = await fetch('/test-alert', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ chat_id })
            });

            const data = await res.json();
            alert(data.message || 'Done');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    if not data:
        return jsonify({'status': 'fail', 'message': 'No data received'})

    try:
        with open('subscribers.json', 'r') as f:
            subscribers = json.load(f)
    except:
        subscribers = []

    subscribers.append(data)

    with open('subscribers.json', 'w') as f:
        json.dump(subscribers, f, indent=4)

    return jsonify({'status': 'success'})

@app.route('/test-alert', methods=['POST'])
def test_alert():
    from telegram import Bot

    data = request.json
    chat_id = data.get('chat_id')
    if not chat_id:
        return jsonify({'message': 'No chat ID provided'})

    # Your bot token
    bot_token = "8239634152:AAHB23IElJeo5xx9pSHTmdAMiI_DZiOHQbc"  # Replace with your real token
    bot = Bot(token=bot_token)

    try:
        bot.send_message(chat_id=chat_id, text="✅ Test Alert: Your subscription system works!")
        return jsonify({'message': 'Test alert sent!'})
    except Exception as e:
        return jsonify({'message': f'Error sending message: {e}'})

if __name__ == '__main__':
    # This port is needed for Render
    app.run(host='0.0.0.0', port=10000)
