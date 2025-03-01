import random

class Stock:
    def __init__(self, symbol, initial_price):
        self.symbol = symbol
        self.price = initial_price

    def update_price(self):
        # Simulate price fluctuation
        change_percent = random.uniform(-0.1, 0.1)  # -10% to +10% change
        self.price *= (1 + change_percent)
        self.price = round(self.price, 2)  # Round to 2 decimal places

class Player:
    def __init__(self, name, initial_money):
        self.name = name
        self.money = initial_money
        self.portfolio = {}  # {symbol: shares}

    def buy_stock(self, stock, shares):
        cost = stock.price * shares
        if self.money >= cost:
            self.money -= cost
            self.portfolio[stock.symbol] = self.portfolio.get(stock.symbol, 0) + shares
            print(f"{self.name} bought {shares} shares of {stock.symbol} at ${stock.price} each.")
        else:
            print(f"{self.name} doesn't have enough money to buy {shares} shares of {stock.symbol}.")

    def sell_stock(self, stock, shares):
        if self.portfolio.get(stock.symbol, 0) >= shares:
            self.money += stock.price * shares
            self.portfolio[stock.symbol] -= shares
            print(f"{self.name} sold {shares} shares of {stock.symbol} at ${stock.price} each.")
            if self.portfolio[stock.symbol] == 0:
                del self.portfolio[stock.symbol]
        else:
            print(f"{self.name} doesn't have enough shares of {stock.symbol} to sell.")

    def get_portfolio_value(self, stocks):
      total = self.money
      for symbol, shares in self.portfolio.items():
        stock = next((s for s in stocks if s.symbol == symbol), None)
        if stock:
          total += stock.price * shares
      return round(total,2)

def main():
    # Game setup
    stocks = [
        Stock("ABC", 100),
        Stock("DEF", 50),
        Stock("GHI", 25),
    ]
    player = Player("Player 1", 1000)
    num_turns = 10

    # Game loop
    for turn in range(num_turns):
        print(f"\n--- Turn {turn + 1} ---")

        # Update stock prices
        for stock in stocks:
            stock.update_price()
            print(f"{stock.symbol}: ${stock.price}")

        #Player actions
        print(f"{player.name}'s current money ${player.money}, Current net worth ${player.get_portfolio_value(stocks)}")
        player_action = input(f"{player.name} would you like to buy or sell? (b/s/n): ")
        if player_action == 'b':
          player_stock = input(f"Which stock would you like to buy? (ABC, DEF, GHI):")
          player_shares = int(input("How many shares would you like to buy?:"))
          stock = next((s for s in stocks if s.symbol == player_stock), None)
          if stock:
            player.buy_stock(stock, player_shares)
          else:
             print("Invalid stock symbol.")
        elif player_action == 's':
          player_stock = input(f"Which stock would you like to sell? (ABC, DEF, GHI):")
          player_shares = int(input("How many shares would you like to sell?:"))
          stock = next((s for s in stocks if s.symbol == player_stock), None)
          if stock:
            player.sell_stock(stock, player_shares)
          else:
             print("Invalid stock symbol.")
        elif player_action != 'n':
            print("Invalid action.")

        print(f"Current Portfolio: {player.portfolio}")
    print(f"\n--- Game Over ---")
    print(f"{player.name}'s net worth is ${player.get_portfolio_value(stocks)}")
    

if __name__ == "__main__":
    main()
