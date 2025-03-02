# Flask stuff for API connection to webapp
from flask import Flask, render_template, request, jsonify, session, url_for
import random
from copy import deepcopy
from stock_data import get_stock_trends
from gemini_ai import generate_data, game_start_gen
from stock_data import get_stock_trends
from test import *
import os
from dotenv import load_dotenv
import json

temp_dict = dict()
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
        "session": temp_dict
        })

# to update session data
@app.route("/update_session", methods=["PUT"])
def update_session():
    """Update session data (e.g., after a trade or week progression)"""
    data = request.json
    temp_dict["user"] = data.get("user", temp_dict["user"])
    temp_dict["current_period"] = data.get("current_period", temp_dict["current_period"])
    temp_dict["companies"] = data.get("companies", temp_dict["companies"])
    return jsonify({"message": "Session updated", "session": temp_dict})

# Initialize session data
def initialize_game(username):
    session["current_period"] = 1
    session["user"] = {
    "username": username,
    "balance": 10000,
    "portfolio": dict()
    }

    ### Initialize companies
    periods, stocks = game_start_gen()

    session["companies"] = dict()
    for res in stocks.keys():
        session["companies"][res] = dict()
        session["companies"][res] = stocks[res]

    session["corp_names"] = list(stocks.keys())

    for z in range(1, 11):
        session[z] = periods[z]

    # Initialize user portfolio
    for res in stocks.keys():
        session["user"]["portfolio"][res] = dict()
        session["user"]["portfolio"][res] = { 
                                            "amount": 0, 
                                            "spent": 0,
                                            "earned": 0 
                                            }
    temp_dict = session
    session.clear()

def contains_tuple(data):
    """Perform a DFS search on nested dictionaries to find a tuple."""
    stack = [data]  # Stack for iterative DFS

    while stack:
        current = stack.pop()  # Get the last added element (LIFO)

        if isinstance(current, dict):  # If it's a dictionary, explore its values
            stack.extend(current.values())  # Add values to the stack
        
        elif isinstance(current, list):  # If it's a list, explore its elements
            stack.extend(current)
        
        elif isinstance(current, tuple):  # If it's a tuple, return True
            return True

    return False  # No tuple found

## -------------------- GAME LOGIC --------------------

# Menu page
@app.route("/")
def menu():
    return render_template("menu.html")

# Start a new game
@app.route("/start_game", methods=["POST"])
def start_game():
    username = request.json.get("username", "Player")  # Get username from JSON
    initialize_game(username)

    return jsonify({"redirect": "/game"})  # Return JSON response with redirect URL

@app.route("/game")
def game_page():
    return render_template("game.html")  # Serve game.html

# End game
@app.route("/end_game")
def end_game():
    session.clear()  # Clear session data
    temp_dict.clear()  # Clear the real (temp) dictionary of data ;)
    return render_template("menu.html")

# Get company names
@app.route("/companies", methods=["GET"])
def get_companies():
    return jsonify({"names": session["corp_names"]})

# Buy stock
@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json["stock"]
    period = int(request.json["current_period"])
    amount = int(request.json["amount"])
    
    price = temp_dict[period][stock]["curr_price"]
    total_cost = amount * price

    if temp_dict["user"]["balance"] >= total_cost:
        temp_dict["user"]["portfolio"][stock]["amt"] += amount
        temp_dict["user"]["portfolio"][stock]["spent"] += total_cost
        temp_dict["user"]["balance"] -= total_cost
        return jsonify({"message": "Stock purchased successfully", "user": temp_dict["user"]})
    else:
        return jsonify({"error": "Not enough balance"}), 400

# Sell stock
@app.route("/sell", methods=["POST"])
def sell():
    stock = request.json["stock"]
    amount = int(request.json["amount"])

    price = temp_dict["companies"][stock]["price"]
    total_cost = amount * price

    if temp_dict["user"]["portfolio"][stock]["amt"] >= amount:
        temp_dict["user"]["portfolio"][stock]["amt"] -= amount
        temp_dict["user"]["portfolio"][stock]["earned"] += total_cost
        temp_dict["user"]["balance"] += total_cost
        return jsonify({"message": "Stock sold successfully", "user": temp_dict["user"]})
    else:
        return jsonify({"error": "Not enough stock to sell"}), 400

# Advance forward in time
@app.route("/advance")
def advance():
    if temp_dict["current_period"] < 7:
        temp_dict["current_period"] += 1

        return jsonify({"current_period": (temp_dict["current_period"] + 1), "session": temp_dict})
    else:
        return jsonify({"game_over": True, "final_balance": temp_dict["user"]["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
