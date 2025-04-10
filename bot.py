# Import required libraries
import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

# Load environment variables
load_dotenv()

# Get API keys
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Initialize clients
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
data_client = CryptoHistoricalDataClient()

def get_account_info():
    account = trading_client.get_account()
    return {
        "equity": account.equity,
        "cash": account.cash,
        "buying_power": account.buying_power
    }

def get_last_trade():
    try:
        with open("trade_log.json", "r") as f:
            lines = f.readlines()
            if lines:
                last_trade = json.loads(lines[-1])
                return last_trade
    except FileNotFoundError:
        pass
    return {
        "symbol": "BTC/USD",
        "action": "none",
        "price": "0",
        "status": "no trades yet"
    }

def get_recent_prices(symbol="BTC/USD"):
    end = datetime.now()
    start = end - timedelta(hours=24)  # Last 24 hours of data

    bars = data_client.get_crypto_bars(symbol, TimeFrame.Minute, start=start, end=end)
    
    if bars.df.empty:
        return []
    
    prices = bars.df['close'].tolist()
    return prices

def ask_deepseek_ai(prices):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"You are an expert crypto trading assistant.\n\n"
        f"Here is the last 24 hours of BTC/USD closing prices:\n{prices}\n\n"
        "Analyze the price trends, patterns, and market conditions. "
        "Consider factors like price momentum, support/resistance levels, and recent volatility. "
        "Based on this analysis, should I BUY, SELL, or HOLD right now? "
        "Reply with only one word: BUY, SELL, or HOLD."
    )

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You help crypto bots make trading decisions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content'].strip().lower()
        return reply
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        return "hold"

def place_trade(symbol, side):
    if side not in ["buy", "sell"]:
        return "No action taken."

    try:
        order = MarketOrderRequest(
            symbol=symbol,
            qty=1,
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )

        trade = trading_client.submit_order(order)
        return f"{side.upper()} order placed for {symbol}"
    except Exception as e:
        return f"Error placing trade: {str(e)}"

def run_bot_cycle(symbol="BTC/USD"):
    prices = get_recent_prices(symbol)

    if not prices:
        return {"error": "No price data received."}

    decision = ask_deepseek_ai(prices)
    result = place_trade(symbol, decision)

    # Log the decision
    log = {
        "time": datetime.now().isoformat(),
        "symbol": symbol,
        "decision": decision,
        "action_taken": result,
        "last_price": prices[-1] if prices else None
    }

    # Save to JSON file
    try:
        with open("trade_log.json", "a") as f:
            f.write(json.dumps(log) + "\n")
    except Exception as e:
        print(f"Error logging trade: {e}")

    print(f"AI decided: {decision.upper()} → {result}")
    return log 