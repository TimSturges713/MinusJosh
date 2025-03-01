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

function getSessionData() {
    fetch('/get_session')
        .then(response => response.json())
        .then(data => {
            console.log('Session data:', data);
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