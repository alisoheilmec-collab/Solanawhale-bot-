import os
import time
import requests
import threading
from flask import Flask

# -------------------- Telegram Info --------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# -------------------- Flask App (for Render keep-alive) --------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# -------------------- Main Bot Logic --------------------
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending message:", e)

def track_solana_whales():
    MIN_BUY_USD = 5000
    MIN_LIQUIDITY_USD = 20000

    while True:
        try:
            # در اینجا باید API یا منبع داده خودت برای تراکنش‌ها رو صدا بزنی
            # این فقط یک مثال تستی هست
            example_trade = {"buy_amount": 6000, "liquidity": 25000, "token": "ExampleToken"}
            
            if example_trade["buy_amount"] >= MIN_BUY_USD and example_trade["liquidity"] >= MIN_LIQUIDITY_USD:
                msg = f"🐋 Whale Alert!\nToken: {example_trade['token']}\nBuy: ${example_trade['buy_amount']}\nLiquidity: ${example_trade['liquidity']}"
                send_telegram_message(msg)
            
            time.sleep(10)
        except Exception as e:
            print("Error tracking:", e)
            time.sleep(5)

# -------------------- Keep-Alive Internal Pinger --------------------
def ping_self():
    while True:
        try:
            render_url = os.environ.get("RENDER_EXTERNAL_URL")
            if render_url:
                requests.get(render_url)
        except:
            pass
        time.sleep(300)  # هر ۵ دقیقه یک بار

# -------------------- Start Everything --------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=ping_self).start()
    track_solana_whales()
