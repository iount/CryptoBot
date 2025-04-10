# Import required libraries
import os  # lets us work with environment variables
from dotenv import load_dotenv  # helps load the .env file with secret keys
from alpaca.trading.client import TradingClient  # Alpaca SDK for trading
from alpaca.trading.requests import MarketOrderRequest  # For creating market orders
from alpaca.trading.enums import OrderSide, TimeInForce  # Trade settings

# Load your secret keys from .env file
load_dotenv()

# Get keys from the environment (safer than writing them in the code)
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Connect to Alpaca using paper trading mode (real trades = paper=False)
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

# Define a function to fetch account info
def get_account_info():
    account = trading_client.get_account()
    # Return only a few important things to keep it simple
    return {
        "equity": account.equity,  # total account value
        "cash": account.cash,  # how much uninvested cash you have
        "buying_power": account.buying_power  # how much you can buy
    }

# Define a function to simulate getting your last trade (just a placeholder)
def get_last_trade():
    return {
        "symbol": "BTC/USD",
        "action": "buy",
        "price": "26500",
        "status": "simulated"  # for now, this isn't linked to real trades
    } 