from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
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

class Company(BaseModel):
    name: str
    stock_value: float
    stock_acronym: str


# Generate AI headlines for company stories
def generate_data(company_data, company_name):
    headline = ""

    prompt = f"""
    Given the company and their previous headlines (if any):
    - Previous headlines: ${company_data}
    - Company name: ${company_name}


    Generate a short news headline that may be randomly negative or positive on changes within the company.
    Usually either will be focused on staff misconduct, or new innovations, or any other form of common headline
    that may be made about a company. The company may have previous headlines, if so make the new headline based off
    previous ones, the company can learn from their previous mistakes or go further into failure, you decide. Then give 
    the new headline for the company. There's only one new headline generated
    for the company. The headline will be the title, and any added details
    will be the details. Put the headline in the title part of the JSON object, and the details in the details
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
        comments[i] = generate_comment(headline, public_perception)
    return headline, comments, public_perception, technical_impact



def generate_comment(headline, public_perception):
    prompt = f"""
    Given the headline for a company's recent news report and the public's perception of the company's changes,
    (Note: the public perception is an integer from 1-20, 1 being most negative, 20 vice versa):
    - HEADLINE: ${headline}
    - PUBLIC_PERCEPTION: ${public_perception}

    Write a comment that may be made from viewers online looking at the headline's story.
    This comment will align with the public's perception and accurately describe how they feel.
    Depending on how aligned this comment is with the public's views, the more likes they'll have.
    Format this answer into a JSON object with comment and likes as the two attributes in the object.
    I'm gonna prompt this prompt multiple times, so don't fall into patterns when generating these comments.
    Pretend that there's been multiple comments produced beforehand so make sure each one you make is unique.
    Choose a random personality out of a list of personalities, pretend like you're writing as a person with that personality.
    Go in depth with how someone may view this headline with that personality, don't be surface level, get deep inside that 
    character and come up with a distinct comment.
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
    
    prompt = f"""
    Retrieve ten random made-up companies (with one word names, limit to 13 characters), their stock market acronym and their respective stock costs.
    Then list the company's names and their stock prices and their acronym in a JSON object. The stock price is between 1 cent and 1000 dollars.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        generated_text = response.text
        data = json.loads(generated_text)
        return data
    except Exception as e:
        return "GEMINI AI RESPONSE FAILURE"