class Stock {
    constructor(symbol, initialPrice) {
      this.symbol = symbol;
      this.price = initialPrice;
    }
  
    updatePrice() {
      // Simulate price fluctuation
      const changePercent = Math.random() * 0.2 - 0.1; // -10% to +10% change
      this.price *= 1 + changePercent;
      this.price = parseFloat(this.price.toFixed(2)); // Round to 2 decimal places
    }
  }
  
  class Player {
    constructor(name, initialMoney) {
      this.name = name;
      this.money = initialMoney;
      this.portfolio = {}; // {symbol: shares}
    }
  
    buyStock(stock, shares) {
      const cost = stock.price * shares;
      if (this.money >= cost) {
        this.money -= cost;
        this.portfolio[stock.symbol] = (this.portfolio[stock.symbol] || 0) + shares;
        console.log(
          `${this.name} bought ${shares} shares of ${stock.symbol} at $${stock.price} each.`
        );
      } else {
        console.log(
          `${this.name} doesn't have enough money to buy ${shares} shares of ${stock.symbol}.`
        );
      }
    }
  
    sellStock(stock, shares) {
      if ((this.portfolio[stock.symbol] || 0) >= shares) {
        this.money += stock.price * shares;
        this.portfolio[stock.symbol] -= shares;
        console.log(
          `${this.name} sold ${shares} shares of ${stock.symbol} at $${stock.price} each.`
        );
        if (this.portfolio[stock.symbol] === 0) {
          delete this.portfolio[stock.symbol];
        }
      } else {
        console.log(
          `${this.name} doesn't have enough shares of ${stock.symbol} to sell.`
        );
      }
    }
  
    getPortfolioValue(stocks) {
      let total = this.money;
      for (const symbol in this.portfolio) {
        const shares = this.portfolio[symbol];
        const stock = stocks.find((s) => s.symbol === symbol);
        if (stock) {
          total += stock.price * shares;
        }
      }
      return parseFloat(total.toFixed(2));
    }
  }
  
  async function main() {
    // Game setup
    const stocks = [
      new Stock("ABC", 100),
      new Stock("DEF", 50),
      new Stock("GHI", 25),
    ];
    const player = new Player("Player 1", 1000);
    const numTurns = 10;
  
    // Game loop
    for (let turn = 0; turn < numTurns; turn++) {
      console.log(`\n--- Turn ${turn + 1} ---`);
  
      // Update stock prices
      for (const stock of stocks) {
        stock.updatePrice();
        console.log(`${stock.symbol}: $${stock.price}`);
      }
  
      // Player actions
      console.log(
        `${player.name}'s current money $${player.money}, Current net worth $${player.getPortfolioValue(
          stocks
        )}`
      );
      
      const playerAction = await askQuestion(`${player.name} would you like to buy or sell? (b/s/n): `);
  
      if (playerAction === "b") {
        const playerStock = await askQuestion("Which stock would you like to buy? (ABC, DEF, GHI): ");
        const playerShares = parseInt(await askQuestion("How many shares would you like to buy?: "));
        const stock = stocks.find((s) => s.symbol === playerStock);
        if (stock) {
          player.buyStock(stock, playerShares);
        } else {
          console.log("Invalid stock symbol.");
        }
      } else if (playerAction === "s") {
        const playerStock = await askQuestion("Which stock would you like to sell? (ABC, DEF, GHI): ");
        const playerShares = parseInt(await askQuestion("How many shares would you like to sell?: "));
        const stock = stocks.find((s) => s.symbol === playerStock);
        if (stock) {
          player.sellStock(stock, playerShares);
        } else {
          console.log("Invalid stock symbol.");
        }
      } else if (playerAction !== "n") {
        console.log("Invalid action.");
      }
  
      console.log(`Current Portfolio: ${JSON.stringify(player.portfolio)}`);
    }
  
    console.log(`\n--- Game Over ---`);
    console.log(`${player.name}'s net worth is $${player.getPortfolioValue(stocks)}`);
  }
  //Helper function to get user input
  const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    
    function askQuestion(query) {
      return new Promise((resolve) => {
        readline.question(query, (ans) => {
          resolve(ans);
        });
      });
    }
  
  main().then(() => readline.close());
  