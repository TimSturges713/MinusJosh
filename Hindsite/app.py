# Flask stuff for API connection to webapp
from flask import Flask, render_template, request, jsonify, session
import random
from copy import deepcopy
from stock_data import get_mock_stock_trends
from gemini_ai import generate_data, get_gemini_initial_data
from stock_data import get_stock_trends
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")  # Required for session handling

## -------------------- SESSION DATA FUNCTIONS --------------------

# to retrieve session data
@app.route("/get_session", methods=["GET"])
def get_session():
    """Retrieve session data for frontend"""
    return jsonify({
        "user": session["user"],
        "current_period": session["current_period"],
        "companies": session["companies"],
        "industries": session["industries"]
        })

# to update session data
@app.route("/update_session", methods=["PUT"])
def update_session():
    """Update session data (e.g., after a trade or week progression)"""
    data = request.json
    session["user"] = data.get("user", session["user"])
    session["current_period"] = data.get("current_period", session["current_period"])
    session["companies"] = data.get("companies", session["companies"])
    return jsonify({"message": "Session updated", "session": session})

# Initialize session data
def initialize_game(gamemode, username):
    session["current_period"] = 1
    session["user"] = {
    "username": username,
    "balance": 10000,
    "portfolio": {}
    }

    ### Initialize companies and industries
    gemini_init_data = game_start_gen(gamemode)
    session["industries"] = gemini_init_data["industries"]
    session["companies"] = gemini_init_data["companies"]

    # Company data structure setup
    # session["companies"][company_name]["price"] = current_stock_cost
    # session["companies"][company_name]["industry"] = industry_name
    # session["companies"][company_name]["employees"] = num_of_employees
    # session["companies"][company_name]["stock_name"] = acronym
    # session["companies"][company_name]["history"][period_num] = {
    #                                                             "headline": "Headline text",
    #                                                             "comments": {comment:"Comment text", likes:likes_amt},  {comment:"Comment text", likes:likes_amt}, ...},
    #                                                             "price": stock_cost
    #                                                             }

    # Initialize user portfolio
    for company in session["companies"].keys():    
        session["user"]["portfolio"][company] = { 
                                            "amount": 0, 
                                            "profit": 0 
                                            }

## -------------------- GAME LOGIC --------------------

# Menu page
@app.route("/")
def menu():
    return render_template("menu.html")

# Start a new game
@app.route("/start_game", methods=["POST"])
def start_game():
    gamemode = request.form.get("gamemode", "default")  # Get gamemode
    username = request.form.get("username", "Player")  # Get username
    initialize_game(gamemode, username)
    gamemode = "game.html" # Choose which gamemode to play (for now only default)
    return render_template(gamemode)

# End game
@app.route("/end_game")
def end_game():
    session.clear()  # Clear session data
    return render_template("menu.html")

# Buy stock
@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json["stock"]
    amount = int(request.json["amount"])
    
    price = session["companies"][stock]["price"]
    total_cost = amount * price

    if session["user"]["balance"] >= total_cost:
        session["user"]["portfolio"][stock]["amount"] += amount
        session["user"]["portfolio"][stock]["profit"] -= total_cost
        session["user"]["balance"] -= total_cost
        return jsonify({"message": "Stock purchased successfully", "user": session["user"]})
    else:
        return jsonify({"error": "Not enough balance"}), 400

# Sell stock
@app.route("/sell", methods=["POST"])
def sell():
    stock = request.json["stock"]
    amount = int(request.json["amount"])

    price = session["companies"][stock]["price"]
    total_cost = amount * price

    if session["user"]["portfolio"][stock]["amount"] >= amount:
        session["user"]["portfolio"][stock]["amount"] -= amount
        session["user"]["portfolio"][stock]["profit"] += total_cost
        session["user"]["balance"] += total_cost
        return jsonify({"message": "Stock sold successfully", "user": session["user"]})
    else:
        return jsonify({"error": "Not enough stock to sell"}), 400

# Advance forward in time
@app.route("/advance")
def advance():
    if session["current_period"] < 7:
        session["current_period"] += 1
        for company in session["companies"].keys():
            headline, comments, public_perception, technical_impact = generate_data(session[company], company)
            new_price = get_stock_trends(headline, comments, public_perception, technical_impact)
            session["companies"][company]["price"] = new_price
            session["companies"][company]["history"][session["current_period"]]["headline"] = headline
            session["companies"][company]["history"][session["current_period"]]["comments"] = comments
            session["companies"][company]["history"][session["current_period"]]["price"] = new_price

        return jsonify({"current_period": (session["current_period"] + 1), "session": session})
    else:
        return jsonify({"game_over": True, "final_balance": session["user"]["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
