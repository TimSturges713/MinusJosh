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
    Given the company and their previous headlines (if any):
    - Previous headlines: ${company_data}
    - Company name: ${company_name}


    Generate a short update or news announcement/headline on the company that may be randomly positive, negative, or neutral on changes within the company. Updates can range for simple, normal quiet announcements, to un-expected important events.
    The company may have previous headlines, if so make the new headline based off previous ones, assuming at least 6 months have past between each headline, and its been more than 6 months since the most recent headline, the company can learn from their previous mistakes or go further into failure, you decide. Then give 
    the new headline for the company. There's only one new headline generated for the company. 
    The headline will be the title, and any added details will be the details. 
    Put the headline in the title part of the JSON object, and the details in the details
    part of the JSON object. Return this in a JSON object.
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
    comments = [None] * num_of_comments
    for i in range(0, num_of_comments):
        comments[i] = generate_comment(headline, public_perception, comments)
    return headline, comments, public_perception, technical_impact


def generate_comment(headline, public_perception, old_comments):
    prompt = f"""
    Given the headline for a company's recent news report and the public's perception of the company's changes,
    (Note: the public perception is an integer from 1-20, 1 being most negative, 20 vice versa):
    - HEADLINE: ${headline}
    - PUBLIC_PERCEPTION: ${public_perception}
    - OTHER COMMENTS (IF ANY): ${old_comments}

    Write a comment that may be made from viewers online looking at the headline's story.
    This comment will align with the public's perception and accurately describe how they feel. The comment should be limited to 2 sentences.
    Depending on how aligned this comment is with the public's views, the more likes they'll have. For example, if the headline is negative and depicts a company in a bad light, the public perception will be low, and comments with negative takes should have high likes, and vice versa if the headline paints the company in a good light.
    Format this answer into a JSON object with comment and likes as the two attributes in the object.
    Choose a random personality out of a long list of personalities, pretend like you're writing as a person with that personality.
    Go in depth with how someone may view this headline with that personality, don't be surface level, get deep inside that 
    character and come up with a distinct comment. Make the comment different than the old comments if there are any. Avoid using same phrasing and speech patterns.
    Try and avoid describing yourself, or things that follow the pattern of "As a ______" or "With a job in _______". Just write the comment as if you were the person you're pretending to be.
    Remember that even though the public may find an announcement good, they may still have negative comments, and vice versa. Just make sure that
    in these cases, the comments that don't align with the public's perception have less likes. Make sure that at least one comment supports the public's perception, and at least one comment does not.
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
        return "GEMINI AI RESPONSE FAILURE"
    

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
        return "GEMINI AI RESPONSE FAILURE"




comp_dat = {"price": 192, "industry": "Military", "employees": 342, "history": {}}


company_n = "Appian Technologies"
head, com, public, technical = generate_data(comp_dat, company_n)
print(f"\nHEADLINE: {head.title}\nDETAILS: {head.detail}\n")
print("COMMENTS:")
for commment in com:
    print(f"\t{commment.likes} likes: {commment.comment}\n\n")

print(f"PUBLIC PERCEPTION: {public}\n")
print(f"TECHNICAL IMPACT: {technical}\n\n")