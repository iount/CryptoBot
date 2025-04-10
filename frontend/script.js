// This function loads account info from your backend Flask server
function loadAccountInfo() {
  // Call the Flask API route /account
  fetch('/account')
    .then(response => response.json()) // Convert the response to JSON
    .then(data => {
      // Set the HTML content with the data we got
      document.getElementById('equity').textContent = `$${parseFloat(data.equity).toFixed(2)}`;
      document.getElementById('cash').textContent = `$${parseFloat(data.cash).toFixed(2)}`;
      document.getElementById('buyingPower').textContent = `$${parseFloat(data.buying_power).toFixed(2)}`;
    });
}

// This function loads trade history
function loadTradeInfo() {
  fetch('/last-trade')
    .then(response => response.json())
    .then(data => {
      document.getElementById('symbol').textContent = data.symbol;
      document.getElementById('action').textContent = data.action;
      document.getElementById('price').textContent = data.last_price ? `$${data.last_price}` : 'N/A';
      document.getElementById('status').textContent = data.action_taken || 'No trades yet';
    });
}

// Function to run the bot and update the display
function runBot() {
  fetch('/run-bot')
    .then(response => response.json())
    .then(data => {
      // Update the trade info with the latest decision
      document.getElementById('symbol').textContent = data.symbol;
      document.getElementById('action').textContent = data.decision;
      document.getElementById('price').textContent = data.last_price ? `$${data.last_price}` : 'N/A';
      document.getElementById('status').textContent = data.action_taken;
      
      // Reload account info to show updated balances
      loadAccountInfo();
    })
    .catch(error => {
      console.error('Error running bot:', error);
      document.getElementById('status').textContent = 'Error running bot';
    });
}

// Run both functions when the page loads
window.onload = () => {
  loadAccountInfo();
  loadTradeInfo();
}; 