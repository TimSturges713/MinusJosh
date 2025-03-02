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
def initialize_game(username):
    session["current_period"] = 1
    session["user"] = {
    "username": username,
    "balance": 10000,
    "portfolio": {}
    }
    session["companies"] = dict()

    ### Initialize companies
    periods, stocks = game_start_gen()
    for res in stocks:
        session["companies"][res["name"]] = res

    # Company data structure setup
    # session["companies"][company_name]["name"] = company_name # ik its redundant but its here so deal w/ it
    # session["companies"][company_name]["price"] = current_stock_cost
    # session["companies"][company_name]["employees"] = num_of_employees
    # session["companies"][company_name]["stock_name"] = acronym
    # }

    # Initialize user portfolio
    for company in session["companies"].keys():    
        session["user"]["portfolio"][company] = { 
                                            "amount": 0, 
                                            "spent": 0,
                                            "earned": 0 
                                            }

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
    return render_template("menu.html")

# Buy stock
@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json["stock"]
    period = int(request.json["current_period"])
    amount = int(request.json["amount"])
    
    price = session[period][stock]["curr_price"]
    total_cost = amount * price

    if session["user"]["balance"] >= total_cost:
        session["user"]["portfolio"][stock]["amt"] += amount
        session["user"]["portfolio"][stock]["spent"] += total_cost
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

    if session["user"]["portfolio"][stock]["amt"] >= amount:
        session["user"]["portfolio"][stock]["amt"] -= amount
        session["user"]["portfolio"][stock]["earned"] += total_cost
        session["user"]["balance"] += total_cost
        return jsonify({"message": "Stock sold successfully", "user": session["user"]})
    else:
        return jsonify({"error": "Not enough stock to sell"}), 400

# Advance forward in time
@app.route("/advance")
def advance():
    if session["current_period"] < 7:
        session["current_period"] += 1

        return jsonify({"current_period": (session["current_period"] + 1), "session": session})
    else:
        return jsonify({"game_over": True, "final_balance": session["user"]["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
