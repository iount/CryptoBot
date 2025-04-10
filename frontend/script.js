// Initialize Chart.js
let performanceChart;
let tradeHistory = [];

// Function to show trade notifications
function showTradeNotification(message, isProfit) {
  Toastify({
    text: message,
    duration: 5000,
    gravity: "top",
    position: "right",
    style: {
      background: isProfit ? "linear-gradient(to right, #00b09b, #96c93d)" : "linear-gradient(to right, #ff416c, #ff4b2b)",
      borderRadius: "5px",
      boxShadow: "0 0 10px rgba(0,0,0,0.3)"
    }
  }).showToast();
}

// Function to update the performance chart
function updatePerformanceChart() {
  const ctx = document.getElementById('performanceChart').getContext('2d');
  
  if (performanceChart) {
    performanceChart.destroy();
  }

  const labels = tradeHistory.map(trade => new Date(trade.time).toLocaleTimeString());
  const data = tradeHistory.map(trade => trade.profit || 0);

  performanceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Profit/Loss',
        data: data,
        borderColor: '#00ff9d',
        backgroundColor: 'rgba(0, 255, 157, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#ffffff'
          }
        }
      }
    }
  });
}

// Function to update account info
function updateAccountInfo() {
  fetch('/account')
    .then(response => response.json())
    .then(data => {
      document.getElementById('equity').textContent = `$${parseFloat(data.equity).toFixed(2)}`;
      document.getElementById('cash').textContent = `$${parseFloat(data.cash).toFixed(2)}`;
      document.getElementById('buyingPower').textContent = `$${parseFloat(data.buying_power).toFixed(2)}`;
    });
}

// Function to update trade history
function updateTradeHistory() {
  fetch('/last-trade')
    .then(response => response.json())
    .then(data => {
      if (data && data.time) {
        // Add new trade to history
        tradeHistory.push(data);
        
        // Update the trade history display
        const historyList = document.getElementById('tradeHistory');
        const tradeItem = document.createElement('div');
        tradeItem.className = 'trade-item';
        
        const profit = data.profit || 0;
        const isProfit = profit >= 0;
        
        tradeItem.innerHTML = `
          <span>${data.symbol} - ${data.decision.toUpperCase()}</span>
          <span class="${isProfit ? 'profit' : 'loss'}">${isProfit ? '+' : ''}$${profit.toFixed(2)}</span>
        `;
        
        historyList.insertBefore(tradeItem, historyList.firstChild);
        
        // Show notification for completed trades
        if (data.action_taken.includes('order placed')) {
          showTradeNotification(
            `${data.symbol}: ${data.decision.toUpperCase()} at $${data.last_price}`,
            isProfit
          );
        }
        
        // Update performance chart
        updatePerformanceChart();
      }
    });
}

// Initialize and start automatic updates
function initializeDashboard() {
  // Initial data load
  updateAccountInfo();
  updateTradeHistory();
  
  // Set up automatic updates
  setInterval(updateAccountInfo, 10000); // Update every 10 seconds
  setInterval(updateTradeHistory, 30000); // Update every 30 seconds
}

// Start the dashboard when the page loads
window.onload = initializeDashboard; 