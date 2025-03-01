# Flask stuff for API connection to webapp
from flask import Flask, render_template, request, jsonify, session
import random
from stock_data import get_mock_stock_trends
from gemini_ai import generate_hints

app = Flask(__name__)

# Menu page
@app.route("/")
def menu():
    return render_template("menu.html")

# Start a new game
@app.route("/start_game", methods=["POST"])
def start_game():
    difficulty = request.form.get("gamemode", "difficulty")  # Get settings
    initialize_game(difficulty)
    gamemode = "game.html" # Choose which gamemode to play (for now only default)
    return render_template(gamemode)

@app.route("/get_game_data")
def get_game_data():
    # Get stock prices for the next week

# Buy stock
@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json["stock"]
    amount = int(request.json["amount"])
    
    price = session["stock_prices"][session["current_week"]][stock] # todo find how to get price (current is probably wrong)
    total_cost = amount * price

    if session["balance"] >= total_cost:
        session["stock"][stock] += amount
        session["balance"] -= total_cost
        # todo: ERROR HANDLER FOR BUYING MORE THAN YOU CAN AFFORD

    return jsonify({"balance": session["balance"], "stocks": session["stocks"]})

# Sell stock
@app.route("/sell", methods=["POST"])
def sell():
    stock = request.json["stock"]
    amount = int(request.json["amount"])
    
    price = session["stock_prices"][session["current_week"]][stock] # todo find how to get price (current is probably wrong)
    total_cost = amount * price

    if session["stocks"][stock] >= amount:
        session["stocks"][stock] -= amount
        session["balance"] += total_cost
        # todo: ERROR HANDLER FOR SELLING MORE THAN YOU HAVE

    return jsonify({"balance": session["balance"], "stocks": session["stocks"]})

# Advance forward in time
@app.route("/advance")
def advance():
    if session["current_week"] < 10:
        session["current_week"] += 1
        return jsonify({"current_week": (session["current_week"] + 1), "hint": session["ai_hints"][session["current_week"]]})
    else:
        return jsonify({"game_over": True, "final_balance": session["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
