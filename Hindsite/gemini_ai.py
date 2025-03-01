from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("GEMENI_KEY"))

# Generate AI hints for stock price changes
def generate_ai_hints(stock_data):
    hints = []

    prompt = f"""
    Given the following stock price changes:
    - TechCorp: ${data["techcorp"]}
    - EcoEnergy: ${data["ecoenergy"]}
    - HyperAuto: ${data["hyperauto"]}

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