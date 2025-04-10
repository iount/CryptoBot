# Importing the necessary Python libraries
from flask import Flask, jsonify, send_from_directory
import os
from bot import get_account_info, get_last_trade

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

# Serve the frontend files
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('frontend', path)

# Run the app (debug mode just helps you see errors during development)
if __name__ == '__main__':
    app.run(debug=True) 