import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text):
    if not BOT_TOKEN:
        print("❌ Telegram токен не задан (TELEGRAM_BOT_TOKEN)")
        return False
    
    if not CHAT_ID:
        print("❌ Chat ID не задан (TELEGRAM_CHAT_ID)")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if not data.get("ok"):
            error_msg = data.get("description", "Unknown error")
            print(f"❌ Telegram API error: {error_msg} (code: {data.get('error_code')})")
            return False
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
