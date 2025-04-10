# Importing the necessary Python libraries
from flask import Flask, jsonify, send_from_directory
import os
from bot import get_account_info, get_last_trade, run_bot_cycle

# Create a Flask app instance (this is the web server)
app = Flask(__name__)

# Define a route (URL) that returns account info when you visit /account
@app.route('/account')
def account():
    return jsonify(get_account_info())  # Call function from bot.py and return as JSON

# Define a route that returns the last trade info when you visit /last-trade
@app.route('/last-trade')
def last_trade():
    return jsonify(get_last_trade())  # Call function from bot.py and return as JSON

# Define a route to run the bot and get its decision
@app.route('/run-bot')
def run_bot_now():
    return jsonify(run_bot_cycle())

# Serve the frontend files
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('frontend', path)

# Get the port from the environment (Render will provide it)
port = int(os.environ.get('PORT', 5000))  # Use 5000 as default if not set

# Run Flask on the public IP and correct port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True) 