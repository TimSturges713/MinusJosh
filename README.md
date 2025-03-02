# MinusJosh
WIC Hackathon Project for Our Team

Name of Program: HindSITE
Description of Program: A stock-market game with predictive analysis performed using Google Gemini. It's a rogue-like stock game where the player goes through a specific number of turns through various stock simulations. The user is given vague headlines from a news source that they must interpret in order to successfully predict the growth and decay of different stocks. There is multiple game modes in more quirky atmospheres, such as Medieval Times and Space, that allows for a more unique experience compared to other stock simulation games out there. It is a short-term game that moves ahead in time for each turn and the highest net worth by the end is the player's high score.

## Inspiration
Our Inspiration for this project was creating something that involved heavy critical thinking, and could hopefully improve the users critical thinking skills. We wanted to use real world situations, especially getting users used to interacting with certain types of datasets. We decided that making a game simulating the stock market would be the best way to achieve this.

## What it does
Our game, HindSite, generates a set of 10 fictional companies across various industries and with various stock prices that you can invest in. Over the course of 10 periods, you may invest and reinvest your seed money of 10,000 across any of the 10 companies. Headlines and comments are generated to hint to users as to how the company may change over the next period, and how the general public feels about each company.

When the user is ready, they can press a "play" button to progress to the next period, and see how their portfolio performed. They then have the opportunity to sell stocks and reinvest their money according to the headlines and comments for the current period. Once all 10 periods have progressed, the game is over and users can see their score. 

## How we built it
Our system is built with a flask back-end to make calls to the Gemini AI, as well as hold the session data for each game. We use simple HTML, CSS, and JavaScript to make the front-end work, with a few functions to interact with our RESTful back-end. The session's data is generated 100% from the start, so there is less time to be spent waiting, and more time to be spend investing!

## Challenges we ran into
Our biggest challenge was wrangling with Gemini AI to give us responses we could do something with. After a long time of struggling with highly repetitive responses, we noticed that when you ask Gemini for multiple examples, they are always unique. And our problem was solved! All we had to do was ask Gemini for a larger amount of responses, and then pick a few randomly each time to increase the originality of events.

Our other greatest challenge is dealing with the massive down time while Gemini AI is "thinking". We solved this by simply pre-generating hundreds of semantic data points into an SQLite database, and then pulling randomly from our database every time a game starts. We then use the data that was grabbed to generate unique datapoints for every game. Think of this strategy like splitting a function with runtime O(n^4), into a function with runtime O(2n^2).

## Accomplishments that we're proud of
We are very proud of how our user interface turned out. Web development and UI design is something that all developers have wrestled with at some point or another. While our UI may not be as responsive as we want it to be we all think it looks great, and without it we wouldn't have our project. 

A stress point in design is the constant battle of trying not to overcomplicate things. Our overall framework only consists of a handful of files, and all of the relevant game data can be sent in a single JSON response. The accomplishment here is having such a detailed product that operates at such a low caliber, and we wouldn't have it any other way.

## What we learned
Not all of our team members were well-versed in web development prior to this project. While this project may not be a "masterclass" in web engineering, it definitely served in boosting our teams knowledge, understanding, and practice in the subject. 

We also learned that Artificial Intelligence definitely isn't as smart as we think it is. There are many flaws with Gemini AI, and we definitely mentioned a few in our "Challenges we ran into" section. Since Artificial Intelligence is a relatively new industry, there are obviously things that will need to be ironed out. But it is without-a-doubt less useful at generative tasks than it is advertised to be. 

## What's next for HindSite
One of the first things we could think of was implementing bids and asks into our game. (Bids and asks allow brokers to set a "maximum buying price" or a "minimum selling price", respectively, that would stay active between periods if the intermittent data meets the bid's or ask's requirements.) This would allow for an even more realistic simulation of the stock market, and even more in-depth thinking for our users.

We also wanted to add a pirate theme or a space theme. (Among many other fun themes.) In these themes you could invest in pirate crews or intergalactic corporations and be given prompts and headlines according to how the possible investment groups may perform. This wouldn't be a functional change, but since all of our semantic data is generated by AI, we would just need to tell the AI to generate headlines and comments for "Black Beard" instead of "Microgreen Solutions".