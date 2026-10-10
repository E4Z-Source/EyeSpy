import time
import threading
import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera

# Pre-configured Telegram Credentials
TELEGRAM_BOT_TOKEN = "8951304151:AAF1_nUdFkgfvtiYWoRlQhv5-voP1Q_EIfE"
TELEGRAM_CHAT_ID = "5022620385"

def send_telegram_message(message):
    """Sends a text log or status update to your Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_telegram_photo(image_path):
    """Uploads and sends a captured image file to your Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        with open(image_path, "rb") as photo_file:
            files = {"photo": photo_file}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": f"Captured: {os.path.basename(image_path)}"}
            requests.post(url, data=data, files=files, timeout=10)
    except Exception as e:
        print(f"Telegram Photo Error: {e}")

class EyeSpyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.label = Label(
            text='EyeSpy Telegram Connected',
            size_hint=(1, 0.15),
            font_size='18sp'
        )
        layout.add_widget(self.label)
        
        self.cam = Camera(
            play=True,
            resolution=(640, 480),
            size_hint=(1, 0.7)
        )
        layout.add_widget(self.cam)
        
        btn = Button(
            text='Take Picture & Send to Telegram',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn.bind(on_press=self.capture_and_send)
        layout.add_widget(btn)
        
        # Start background loop thread
        threading.Thread(target=self.background_monitor_loop, daemon=True).start()
        
        # Send startup notification to Telegram
        threading.Thread(target=lambda: send_telegram_message("EyeSpy App Started Successfully on Device.")).start()
        
        return layout

    def capture_and_send(self, instance):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"IMG_{timestamp}.png"
        
        self.cam.export_to_png(filename)
        self.label.text = f"Saved & Sending: {filename}"
        
        # Send photo asynchronously via thread to avoid freezing the UI
        threading.Thread(target=send_telegram_photo, args=(filename,), daemon=True).start()

    def background_monitor_loop(self):
        while True:
            # Periodic background check sent to Telegram
            send_telegram_message("EyeSpy Status: Background loop running active check.")
            time.sleep(300) # Sends a check-in log every 5 minutes

if __name__ == '__main__':
    EyeSpyApp().run()
