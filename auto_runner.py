import time
import os
import datetime
import json
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoBarsRequest
import requests

# Load your API keys
load_dotenv()
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Alpaca clients
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
data_client = CryptoHistoricalDataClient()

# Symbols to trade
symbols = ["BTC/USD", "ETH/USD"]
interval = 60  # 60 seconds

# Memory of open positions
positions = {}

def get_24h_data(symbol):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=24)

    request_params = CryptoBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end
    )

    bars = data_client.get_crypto_bars(request_params)
    df = bars.df

    if df.empty:
        return []

    return df['close'].tolist()

def get_account_balance():
    try:
        account = trading_client.get_account()
        print(f"Account status: {account.status}")
        print(f"Buying power: {account.buying_power}")
        print(f"Cash: {account.cash}")
        return float(account.cash)
    except Exception as e:
        print(f"Error getting account balance: {e}")
        return 0.0

def get_pnl(entry_price, current_price):
    return round(current_price - entry_price, 2)

def ask_deepseek(symbol, prices, balance, position=None):
    prompt = (
        f"You are a crypto trading AI.\n\n"
        f"Symbol: {symbol}\n"
        f"Balance: ${balance}\n"
        f"Prices (last 24h): {prices[-60:]}\n"  # only recent hour to keep it short
    )

    if position:
        entry = position['entry_price']
        pnl = get_pnl(entry, prices[-1])
        prompt += (
            f"\nYou are currently in a position entered at ${entry}.\n"
            f"Current price: ${prices[-1]}\n"
            f"P&L: ${pnl}\n"
        )
    else:
        prompt += "\nYou currently have no open position.\n"

    prompt += "\nShould the bot BUY, SELL, or HOLD? Respond with just one word."

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You help make crypto trading decisions."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }
    )

    try:
        decision = response.json()['choices'][0]['message']['content'].strip().lower()
        return decision
    except:
        return "hold"

def place_order(symbol, side):
    try:
        order = MarketOrderRequest(
            symbol=symbol,
            qty=1,
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        print(f"Placing {side} order for {symbol}...")
        order_response = trading_client.submit_order(order)
        print(f"Order placed successfully: {order_response}")
        return True
    except Exception as e:
        print(f"Error placing order: {e}")
        return False

def run_bot(symbol):
    try:
        print(f"\n=== Processing {symbol} ===")
        prices = get_24h_data(symbol)
        if not prices:
            print(f"No price data available for {symbol}")
            return

        balance = get_account_balance()
        print(f"Current balance: ${balance}")
        
        # Get current position
        position = None
        try:
            position = trading_client.get_position(symbol)
            print(f"Current position: {position}")
        except:
            print(f"No open position for {symbol}")

        decision = ask_deepseek(symbol, prices, balance, position)
        print(f"AI Decision: {decision}")

        if decision == "buy" and not position:
            if place_order(symbol, "buy"):
                print(f"Successfully bought {symbol}")
        elif decision == "sell" and position:
            if place_order(symbol, "sell"):
                print(f"Successfully sold {symbol}")
        else:
            print(f"Holding {symbol}")

    except Exception as e:
        print(f"Error in run_bot for {symbol}: {e}")

# === MAIN LOOP ===
print("🚀 AI Crypto Bot is running every minute...")
while True:
    for symbol in symbols:
        run_bot(symbol)
    time.sleep(interval) 