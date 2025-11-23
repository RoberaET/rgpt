"""
Keep Alive Server for Replit
Simple Flask server to keep the bot running (for Uptime Robot)
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

@app.route('/health')
def health():
    return {"status": "ok", "service": "telegram-bot"}

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()

