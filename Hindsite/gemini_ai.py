from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

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
def generate_headlines(data):
    headline = ""

    prompt = f"""
    Given the company and their previous headlines (if any):
    - COMPANY1: ${data["COMPANY1"]}

    Generate a short news headline that may be randomly negative or positive on changes within the company.
    Usually either will be focused on staff misconduct, or new innovations, or any other form of common headline
    that may be made about a company. The company may have previous headlines, if so make the new headline based off
    previous ones, the company can learn from their previous mistakes or go further into failure, you decide. Then give 
    the new headline for the company. There's only one new headline generated
    for the company. Start the headline with a '*' character, and 
    end it with a ';' character to show where it begins and ends. The headline will be the title, and any added details
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

def generate_comment(headline, public_perception):
    prompt = f"""
    Given the headline for a company's recent news report and the public's perception of the company's changes,
    (Note: the public perception is an integer from 1-20, 1 being most negative, 20 vice versa):
    - HEADLINE: ${headline}
    - PUBLIC_PERCEPTION: ${public_perception}

    Write 3-5 comments that may be made from viewers online looking at the headline's story.
    These comments will align with the public's perception and accurately describe how they feel.
    Depending on how aligned these comments are with the public's views, the more likes they'll have.
    Format this answer into a JSON object with comment and likes as the two attributes in the object.
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
    public_perception = 0, technical_impact = 0
    prompt = f"""
    Given the following headline JSON object:
    - HEADLINE1: ${data}

    Based on the headline and the way it describes the company's changes and possible problems, 
    generate two constants that describe the public's perception of the company(1-20, 1 being most negative, 20 being most positive)
    and the actual impact the news described in the headline may actually have on the functionality of the company
    from a technical standpoint (1-20, 1 being most negative, 20 being most positive). Please just only give the two numbers, nothing else
    as a response, with the public perception first and the technical impact second. Formatted like i,j just being separated
    by a comma.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        constants = response.text
        constants = constants.split(",")
        for c in constants:
            if c.isdigit():
                if public_perception == 0:
                    public_perception = int(c)
                else:
                    technical_impact = int(c)
        return public_perception, technical_impact

    except Exception as e:
        return "GEMINI AI RESPONSE FAILURE"