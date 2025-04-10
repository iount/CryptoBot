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

// This function loads fake last trade info
function loadTradeInfo() {
  fetch('/last-trade')
    .then(response => response.json()) // Convert the response to JSON
    .then(data => {
      document.getElementById('symbol').textContent = data.symbol;
      document.getElementById('action').textContent = data.action;
      document.getElementById('price').textContent = `$${data.price}`;
      document.getElementById('status').textContent = data.status;
    });
}

// Run both functions when the page loads
window.onload = () => {
  loadAccountInfo();
  loadTradeInfo();
}; 