app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_server, daemon=True).start()

import requests
import time
import os

# متغیرها از Environment Variables در Render خونده میشن
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# آدرس API برای دریافت تراکنش‌های بزرگ (نمونه از birdeye)
API_URL = "https://public-api.birdeye.so/public/large-transactions"

# معیارها
MIN_BUY_USD = 5000
MIN_LIQUIDITY_USD = 20000

HEADERS = {
    "accept": "application/json",
    "x-chain": "solana"
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def check_whale_trades():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        data = response.json()

        for tx in data.get("data", []):
            amount_usd = tx["amountInUsd"]
            liquidity_usd = tx["pool"]["liquidityInUsd"]

            # اعمال فیلترها
            if amount_usd >= MIN_BUY_USD and liquidity_usd >= MIN_LIQUIDITY_USD:
                token_symbol = tx["token"]["symbol"]
                token_address = tx["token"]["address"]
                buyer = tx["account"]
                volume = f"{amount_usd:,.0f} USD"
                liquidity = f"{liquidity_usd:,.0f} USD"

                message = (
                    f"🐋 <b>Whale Buy Detected!</b>\n"
                    f"Token: <b>{token_symbol}</b>\n"
                    f"Value: {volume}\n"
                    f"Liquidity: {liquidity}\n"
                    f"Buyer: {buyer}\n"
                    f"CA: {token_address}"
                )

                send_telegram_message(message)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        check_whale_trades()
        time.sleep(30)  # هر ۳۰ ثانیه یکبار چک کن
