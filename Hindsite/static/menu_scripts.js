function startGame(gamemode) {
    var username = document.getElementById("username").value;
    const data = {
        "gamemode": gamemode,
        "username": username
    };

    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.text())  // Change to text() since Flask returns an HTML page
    .then(() => {
        console.log('Game started');
        window.location.href = "/game";  // Redirect to game.html
    })
    .catch((error) => {
        console.error('Error starting game:', error);
    });
}