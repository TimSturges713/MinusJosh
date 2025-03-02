function updateSessionData(data) {
    fetch('/update_session', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Session updated:', data);
    })
    .catch((error) => {
        console.error('Error updating session:', error);
    });
}

let session = null;

function getSessionData() {
    fetch('/get_session')
        .then(response => response.json())
        .then(data => {

            console.log('Session data:', data);
            session = data;
            let currentPeriod = session.current_period;

            // Initialize chartData for each company
            companies.forEach(company => {
                if (session.companies && session.companies[company]) {
                    let history = session.companies[company].history;

                    chartData[company] = {
                        labels: Array.from({ length: currentPeriod }, (_, i) => i + 1),  // Labels: 1 to currentPeriod
                        data: Object.values(history).slice(0, currentPeriod).map(entry => entry[0]) // Extract prices
                    };
                }
            });
        })
        .catch((error) => {
            console.error('Error getting session data:', error);
        });
}

function buyStock(stock, amount) {
    fetch('/buy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock: stock, amount: amount }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Buy response:', data);
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Error buying stock:', error);
    });
}

function sellStock(stock, amount) {
    fetch('/sell', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock: stock, amount: amount }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sell response:', data);
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Error selling stock,):', error);
    });
}

const chartData = {};

/*  Dynamic Stock Chart  */
getSessionData();

// Get chart canvas
const ctx = document.getElementById('chartCanvas').getContext('2d');

// Create initial chart
let chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: chartData.data1.labels,
        datasets: [{
            label: 'Dataset 1',
            data: chartData.data1.data,
            borderColor: 'blue',
            borderWidth: 2,
            fill: false
        }]
    }
});

// Function to update chart when radio button is clicked
function updateChart(company) {
    const newData = chartData[company];
    chart.data.labels = newData.labels;
    chart.data.datasets[0].label = `${company} Stock Prices`;
    chart.data.datasets[0].data = newData.data;
    chart.update(); // Refresh the chart
}

function next_period(){
    modal = document.getElementById("m")
    modal.style.display = "block";
    fetch('/advance', {
        headers:{
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Advance response:', data);
        if (data.game_over) {
            modal.style.display = "none";
            alert(`Game Over! Final Balance: $${data.final_balance}`);
            fetch('/end_game')
            .then(response => response.text())
            .then(data => {
                window.location.href = "/menu"
            })
            // Optionally redirect to a game over screen or reset the game
        }
        else{
            setTimeout(function() {
                console.log("Waited for 3 seconds");
                // Do something after the delay here
            }, 3000);
            modal.style.display = "none";   
        }
    })
}



// Event listener for radio buttons
document.querySelectorAll('input[name="dataSet"]').forEach(radio => {
    radio.addEventListener('change', (event) => {
        updateChart(event.target.value);
    });
});

