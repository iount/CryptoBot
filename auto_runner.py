import time
from bot import run_bot_cycle

# List of crypto symbols you want to trade
symbols = ["BTC/USD", "ETH/USD", "SOL/USD"]

# How often to trade (in seconds) — adjust this to your preference
interval = 600  # 600 seconds = 10 minutes

# Run forever
while True:
    for symbol in symbols:
        print(f"🔁 Running bot for {symbol}")
        result = run_bot_cycle(symbol)
        print(result)
    print(f"⏱️ Waiting {interval / 60} minutes before next round...")
    time.sleep(interval) 