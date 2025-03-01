# Flask stuff for API connection to webapp
from flask import Flask, render_template, request, jsonify, session
import random
from copy import deepcopy
from stock_data import get_mock_stock_trends
from gemini_ai import generate_hints

app = Flask(__name__)


## Session Data functions

# to create the initial session data
def set_session():
    """Store game data in session"""
    data = request.json
    session["user"]["balance"] = data.get("balance", 10000)
    session["user"]["portfolio"] = data.get("portfolio", defaultdict(tuple))
    session["current_period"] = data.get("current_period", 1)
    session["companies"] = {data["companies"]}
    session["industries"] = data["industries"]
    return jsonify({"message": "Session data set", "session": session})

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

    gemini_generate_companies()

    for company in session["companies"].keys():    
        session["user"]["portfolio"][company] = { 
                                            "amount": 0, 
                                            "profit": 0 
                                            }



    ### Initialize companies and industries
    # match gamemode:
    #     case _: # Default gamemode (normal)   
    #         industries = ["Technology", "Energy", "Automotive", "Healthcare", "Finance"]
    #         com = ["TechCorp", "CyberSecure", "AIFrontier", "EcoEnergy", "GreenFusion", 
    #         "HyperAuto", "DriveWorks", "MediHealth", "BioGenix", "FinTrust", "WealthWell"]
    # session["companies"] = dict()
    # for industry in industries:
    #     session["industries"][industry] = dict()

    # for company in com:
    #     history_dict = {1: tuple((stock_value(company), []))}
    #     random_employee = random.randint(50, 100000) # random employee size
    #     session["companies"][company] = {
    #                                     "price": 100, 
    #                                     "employee_number": random_employee, 
    #                                     "approval_rating": , 
    #                                     "history": history_dict 
    #                                     }


# Menu page
@app.route("/")
def menu():
    return render_template("menu.html")

# End game
@app.route("/end_game")
def end_game():
    session.clear()  # Clear session data
    return render_template("menu.html")

# Start a new game
@app.route("/start_game", methods=["POST"])
def start_game():
    gamemode = request.form.get("gamemode", "default")  # Get gamemode
    username = request.form.get("username", "Player")  # Get username
    initialize_game(gamemode, username)
    gamemode = "game.html" # Choose which gamemode to play (for now only default)
    return render_template(gamemode)

# Buy stock
@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json["stock"]
    amount = int(request.json["amount"])
    
    price = session["company"][stock]["price"]
    total_cost = amount * price

    if session["user"]["balance"] >= total_cost:
        session["user"]["portfolio"][stock]["amount"] += amount
        session["user"]["portfolio"][stock]["profit"] -= total_cost
        session["user"]["balance"] -= total_cost
        # todo: ERROR HANDLER FOR BUYING MORE THAN YOU CAN AFFORD

    return jsonify({"balance": session["user"]["balance"], "stocks": session["stocks"]})

# Sell stock
@app.route("/sell", methods=["POST"])
def sell():
    stock = request.json["stock"]
    amount = int(request.json["amount"])

    price = session["company"][stock][price]
    total_cost = amount * price

    if session["user"]["portfolio"][stock]["amount"] >= amount:
        session["user"]["portfolio"][stock]["amount"] -= amount
        session["user"]["portfolio"][stock]["profit"] += total_cost
        session["user"]["balance"] += total_cost
        # todo: ERROR HANDLER FOR SELLING MORE THAN YOU HAVE

    return jsonify({"balance": session["user"]["balance"], "stocks": session["stocks"]})

# Advance forward in time
@app.route("/advance")
def advance():
    if session["current_period"] < 10:
        session["current_period"] += 1
        return jsonify({"current_period": (session["current_period"] + 1), "hint": session["ai_hints"][session["current_week"]]})
    else:
        return jsonify({"game_over": True, "final_balance": session["user"]["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
