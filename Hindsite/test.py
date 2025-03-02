from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import random

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

class Headline(BaseModel):
    title: str
    detail: str

class Comment(BaseModel):
    comment: str
    likes: int


# Generate AI headlines for company stories
def generate_data(company_data, company_name):
    headline = ""


    prompt = f"""
    Generate a short but unique news headline for the company '{company_name}', considering:
    
    - Previous headlines (if any): {company_data}
    - Assume at least 6 months have passed since the last event.
    - The company can experience **positive, negative, or neutral** events.
    - The event type should vary and not always be the same type as previous headlines.

    Each company should have a mix of financial, leadership, legal, product, and external events.
    #### **💰 Financial Changes (Positive, Neutral, or Negative)**
- The company **announces record-breaking profits**, sending stock prices soaring. 
- A surprise **stock buyback program** boosts share prices. 
- Investors pull out after **unexpected revenue shortfalls**, leading to a sharp drop. 
- The company secures a **billion-dollar investment deal**, creating optimism for expansion.
- Earnings meet expectations, **causing no major stock movement**. 

#### **🏛 Leadership Shifts (Positive, Neutral, or Negative)**
- The **CEO resigns suddenly** after an internal power struggle. 
- A new, **controversial CEO** takes over, sparking debate in the financial community.
- The company appoints a **visionary leader**, implementing a radical strategy. 
- Boardroom shake-up **raises questions about future stability**. 
- A whistleblower reveals **leadership corruption**, forcing resignations.

#### **⚖️ Scandals & Legal Trouble (Mostly Negative, Sometimes Neutral)**
- The company faces a **federal investigation** for financial fraud.
- A former executive is arrested for **embezzlement**, shocking the industry.
- The company reaches **a settlement in a long-standing lawsuit**, ending legal uncertainty.
- A **major cybersecurity breach** exposes millions of customer records. 
- Government regulators approve the company’s **new compliance standards**.

#### **🛠 Major Product Breakthroughs or Failures (Positive, Neutral, or Negative)**
- The company unveils **groundbreaking AI technology**, sending stock soaring.
- A highly anticipated product **fails spectacularly**, leading to mass refunds. 
- A **major competitor beats them to market**, causing investor concern.
- The company’s **new electric vehicle catches fire** during testing, delaying release
- A routine software update **improves efficiency with minor tweaks**. 

#### **🚨 Unexpected Crises (Mostly Negative)**
- The company suffers **a factory fire or natural disaster**, disrupting production. 
- A **sudden cyberattack** forces a shutdown of critical infrastructure. 
- Employee strikes or union protests bring production to a halt.
- International sanctions force the company to **exit key markets**, hurting profits.
- The company mitigates risk by **securing backup production facilities**. 

#### **🏛 Government Regulations & Geopolitical Events (Positive, Neutral, or Negative)**
- New government policies **crack down on industry practices**, forcing restructuring. ve)*
- A major **trade war or tariff** significantly impacts the company’s bottom line. 
- The company **secures a government contract**, leading to financial stability. 
- A new law bans their **flagship product**, sending stocks crashing. 
- Company leadership **meets with regulators to ensure compliance**, preventing fines.

#### **📉 Market Competition & Mergers (Positive, Neutral, or Negative)**
- A **rival company launches an aggressive takeover bid**, making headlines. 
- The company **merges with a competitor**, forming a new industry giant. 
- A small startup disrupts the market, threatening the company's dominance.
- The company is caught **copying a competitor’s technology**, leading to legal trouble.
- A new strategic partnership **boosts market confidence**. 

#### **⚙️ Supply Chain Issues & Production Problems (Positive, Neutral, or Negative)**
- A global semiconductor shortage **delays product rollouts** by months.
- The company’s new manufacturing plant **faces environmental protests**.
- Labor shortages force **a major production slowdown**.
- A **supplier goes bankrupt**, leaving the company scrambling for alternatives.
- The company secures **alternative supply chains**, reducing future risks.

---
    🎯 **Rules for Generation:**
    - Ensure variety: Do not repeat similar types of events multiple times in a row.
    - Do not make every military company about "new contracts" or "autonomous drones."
    - Keep the headline engaging but **not repetitive**.
    - Return only one headline **formatted as JSON**, with:
      - `"title"`: The short, attention-grabbing news headline.
      - `"details"`: A sentence or two expanding on the event.

    Return the response **strictly as a JSON object**.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': Headline,
            },
        )
        headline = response.parsed

    except Exception as e:
        headline = "GEMINI AI RESPONSE FAILURE"
    (public_perception, technical_impact) = generate_trend(headline)
    num_of_comments = random.randint(3,5)
    comments = [None, None, None]
    comments[0] = generate_pos_comment(headline, public_perception, comments)
    comments[1] = generate_pos_comment(headline, public_perception, comments)
    comments[2] = generate_neg_comment(headline, public_perception, comments)
    random.shuffle(comments)
    return headline, comments, public_perception, technical_impact


def generate_pos_comment(headline, public_perception, old_comments):
    prompt = f"""
    Given the headline for a company's recent news report and the public's perception of the company's changes,
    (Note: the public perception is an integer from 1-20, 1 being most negative, 20 vice versa):
    - HEADLINE: ${headline}
    - PUBLIC_PERCEPTION: ${public_perception}
    - OTHER COMMENTS (IF ANY): ${old_comments}

    Write a comment that is from the perspective of a viewer online looking at the headline's story.
    The comment must agree with the public opinion of the company's changes and the headline.
    If the public opinion is less than 10, then the comment must be negative about the headline, and if the public opinion is greater than 10, the comment must be positive about the story.
    This comment, as it agrees with the public opinion, will have a large amount of likes.
    Format this answer into a JSON object with comment and likes as the two attributes in the object.
    Choose a random personality out of a list of personalities, pretend like you're writing as a person with that personality.
    Avoid describing yourself, or things that follow the pattern of "As a ______" or "With a job in _______". Just write the comment as if you were the person you're pretending to be, without describing your current circumstances or occupation.
    Go in depth with how someone may view this headline agrees with public opinion with said personality, don't be surface level, get deep inside that 
    character and come up with a distinct comment.

    🚨 **Do NOT include anything except the JSON response.** No explanations or extra text.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': Comment,
            },
        )
        comment = response.parsed
    except Exception as e:
        comment = "GEMINI AI RESPONSE FAILURE"
    return comment

def generate_neg_comment(headline, public_perception, old_comments):
    prompt = f"""
    Given the headline for a company's recent news report, the public's perception of the company's changes, and the other comments,
    (Note: the public perception is an integer from 1-20, 1 being most negative view of the headline, and 20 being the most positive):
    - HEADLINE: ${headline}
    - PUBLIC_PERCEPTION: ${public_perception}
    - OTHER COMMENTS (IF ANY): ${old_comments}

    Write a comment that is from the perspective of a viewer online looking at the headline's story.
    The comment must disagree with the public opinion of the company's changes and the headline.
    If the public opinion is less than 10, then the comment must be positive about the headline, and if the public opinion is greater than 10, the comment must be negative about the story.
    This comment, as it disagrees with the public opinion, will have a small amount of likes.
    Avoid describing yourself, or things that follow the pattern of "As a ______" or "With a job in _______". Just write the comment as if you were the person you're pretending to be, without describing your current circumstances or occupation.
    Format this answer into a JSON object with comment and likes as the two attributes in the object.
    Choose a random personality out of a list of personalities, pretend like you're writing as a person with that personality.
    Go in depth with how someone may view this headline against public opinion with said personality, don't be surface level, get deep inside that 
    character and come up with a distinct comment.

    🚨 **Do NOT include anything except the JSON response.** No explanations or extra text.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': Comment,
            },
        )
        comment = response.parsed
    except Exception as e:
        comment = "GEMINI AI RESPONSE FAILURE"
    return comment


def generate_trend(data):
    public_perception = 0
    technical_impact = 0
    prompt = f"""
    Given the following headline JSON object:
    - HEADLINE: ${data}

    Based on the headline and the way it describes the company's changes and possible problems, 
    generate two constants that describe the public's perception of the company(1-20, 1 being most negative, 20 being most positive)
    and the actual impact the news described in the headline may actually have on the functionality of the company
    from a technical standpoint (1-20, 1 being most negative, 20 being most positive). Please just only give the two numbers, nothing else
    as a response, with the public perception first and the technical impact second. Formatted like i,j just being separated
    by a comma. Do not specifically mention stock price or its trends, make it more vague and about the event only.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        constants = response.text
        constants = constants.split(",")
        public_perception = int(constants[0])
        technical_impact = int(constants[1])
        return public_perception, technical_impact

    except Exception as e:
        raise "GEMINI AI RESPONSE FAILURE"
    

def game_start_gen():
    stocks = dict()
    prompt = f"""
    Make a list of ten random made-up companies (with one word names less than 30 characters) on the stock market, their stock market acronym, and their respective costs.
    Randomly make these companies stock prices from 1 cent to 1000 dollars.
    Then list the company's names, the stock acronym, and their stock prices. List them with nothing else other than separating company
    name, stock value, and stock acronym by a comma. Each new line is a different company and each line ends with a comma.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        stock = response.text
        stock = stock.split(",")
        flag = 0
        for c in range(0, stocks.length(), 2):
            stocks[stock[c]] = stock[c+1]
        return stocks
    except Exception as e:
        raise "GEMINI AI RESPONSE FAILURE"



comp_dat = {"price": 192, "industry": "Military", "employees": 342, "history": {}}


company_n = "Appian Technologies"
head, com, public, technical = generate_data(comp_dat, company_n)
print(f"\nHEADLINE: {head.title}\nDETAILS: {head.detail}\n")
print("COMMENTS:")
for commment in com:
    print(f"\t{commment.likes} likes: {commment.comment}\n\n")

print(f"PUBLIC PERCEPTION: {public}\n")
print(f"TECHNICAL IMPACT: {technical}\n\n")