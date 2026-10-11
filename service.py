import time
import requests

TOKEN = "8951304151:AAF1_nUdFkgfvtiYWoRlQhv5-voP1Q_EIfE"
CHAT_ID = "5022620385"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        pass

def main():
    # Send a notification when the service boots up
    send_telegram_message("EyeSpy background service has started.")
    
    # Periodic status loop (sends a check-in message every 5 minutes)
    while True:
        send_telegram_message("EyeSpy background service is active.")
        time.sleep(300)

if __name__ == '__main__':
    main()
