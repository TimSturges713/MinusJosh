from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

# Generate AI hints for stock price changes
def generate_hints(stock_data):
    hints = []

    prompt = f"""
    Given the following stock price changes:
    - COMPANY1: ${data["COMPANY1"]}
    - COMPANY2: ${data["COMPANY2"]}
    - COMPANY3: ${data["COMPANY3"]}

    Generate short news headlines that hint at reasons for these changes.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        hints.append(response.text)
    except Exception as e:
        hints.append("GEMINI AI RESPONSE FAILURE")

    return hints

def generate_trend(headline):
    public_perception = 0, technical_impact = 0
    prompt = f"""
    Given the following headlines:
    - HEADLINE1: ${data["HEADLINE1"]}
    - HEADLINE2: ${data["HEADLINE2"]}
    - HEADLINE3: ${data["HEADLINE3"]}

    Based on these headlines and the way they describe the company's changes and possible problems, 
    generate two constants that describe the public's perception of the company(1-20, 1 being most negative, 20 being most positive)
    and the actual impact the news described in the headline may actually have on the functionality of the company
    from a technical standpoint (1-20, 1 being most negative, 20 being most positive). Please just only give the two numbers, nothing else
    as a response, with the public perception first and the technical impact second.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        constants = response.text
        for c in constants:
            if c.isdigit():
                if public_perception == 0:
                    public_perception = int(c)
                else:
                    technical_impact = int(c)
        return public_perception, technical_impact

    except Exception as e:
        return "GEMINI AI RESPONSE FAILURE"