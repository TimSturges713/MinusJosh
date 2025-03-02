function startGame() {
    var username = document.getElementById("username").value || "Player";  // Default to "Player" if empty
    
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username }),  // Send JSON data
    })
    .then(response => response.json())  // Expect JSON response
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;  // Redirect to game.html
        }
    })
    .catch((error) => {
        console.error('Error starting game:', error);
    });
}