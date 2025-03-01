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
    Given the following companies and their stock prices:
    - COMPANY1: ${data["COMPANY1"]}
    - COMPANY2: ${data["COMPANY2"]}
    - COMPANY3: ${data["COMPANY3"]}
    - COMPANY4: ${data["COMPANY4"]}
    - COMPANY5: ${data["COMPANY5"]}
    - COMPANY6: ${data["COMPANY6"]}
    - COMPANY7: ${data["COMPANY7"]}
    - COMPANY8: ${data["COMPANY8"]}
    - COMPANY9: ${data["COMPANY9"]}
    - COMPANY10: ${data["COMPANY10"]}

    Generate short news headlines that may be randomly negative or positive on changes within the company.
    Usually either will be focused on staff misconduct, or new innovations, or any other form of common headline
    that may be made about a company.
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
    - HEADLINE4: ${data["HEADLINE4"]}
    - HEADLINE5: ${data["HEADLINE5"]}
    - HEADLINE6: ${data["HEADLINE6"]}
    - HEADLINE7: ${data["HEADLINE7"]}
    - HEADLINE8: ${data["HEADLINE8"]}
    - HEADLINE9: ${data["HEADLINE9"]}
    - HEADLINE10: ${data["HEADLINE10"]}

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