import json
import time
import requests

BOT_TOKEN = '8239634152:AAHB23IElJeo5xx9pSHTmdAMiI_DZiOHQbc'

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    requests.post(url, data=data)

def check_shows():
    try:
        with open('subscribers.json') as f:
            subscribers = json.load(f)
        with open('chat_ids.json') as f:
            chat_ids = json.load(f)
    except FileNotFoundError:
        return

    for sub in subscribers:
        movie = sub['movie']
        city = sub['city']
        username = sub['username']

        # 🔴 Replace this with actual BookMyShow scraper
        show_available = True  # Mock

        if show_available and username in chat_ids:
            chat_id = chat_ids[username]
            message = f"🎉 A show for *{movie}* is now available in *{city}*! Book fast!"
            send_telegram_message(chat_id, message)

if __name__ == '__main__':
    while True:
        print("🔄 Checking for shows...")
        check_shows()
        time.sleep(60)
