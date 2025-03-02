import sqlite3
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import random
from typing import List  # FIX: Import List for Pydantic model
from test import *

INDUSTRIES = 5
COMPANIES = 4
HEADLINES = 10

class HeadlineArray(BaseModel):
    headlines: List[str]

class IndustryArray(BaseModel):
    industries: List[str]

class CompanyFull(BaseModel):
    name: str
    price: float
    employees: int
    stock_name: str

class GameStart(BaseModel):
    companies: list[CompanyFull]

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

# Database file name
db_name = "small_db.db"
i = 0
def gen_extra_details(conn, headline, public):
    cursor = conn.cursor()
    
    cursor.execute("""SELECT id FROM headlines WHERE headline = ? """, (headline,))
    prompt_id = cursor.fetchone()[0]

    comments = [None, None, None]
    time.sleep(20)
    global i
    print(i)
    i += 1
    if i > 1000000:
        i = 0
    comments[0] = generate_pos_comment(headline, public, comments)
    comments[1] = generate_pos_comment(headline, public, comments)
    time.sleep(2)
    comments[2] = generate_neg_comment(headline, public, comments)
    random.shuffle(comments)

    for idx, comm in enumerate(comments):
        cursor.execute("""
        INSERT INTO comment (id, headline_id, comment, likes)
        VALUES (?, ?, ?, ?)
        """, (idx, prompt_id, comm.comment, comm.likes))
    conn.commit()
    return

def gemini_create_prompts(industry) -> list:
    prompt = f"""
    Using the industry {industry}, generate a list of {HEADLINES} random yet distinct and unique headlines (limit the headlines to 75 characters maximum) that may be positive or negative on changes within the industry. Each headline needs to have a place for a company name in the industry to be inserted. This place where the name will go should have '{{name}}' in its place as a placeholder.
    Put the headline in the 'headline' part of the JSON object, with the key for each being an incrementing int. The returned result will be a json object.

    The format of the json should be     
        ```json
    {{
        "headlines": [
            "Headline 1",
            "Headline 2",
            ...
            "Headline 10"
        ]
    }}
    ```
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': HeadlineArray,
            },
        )
        data = response.parsed
        return data.headlines
    except Exception as e:
        print(e)
        print("GEMINI AI RESPONSE FAILURE")
        return []

def gemini_create_industries() -> list:
    prompt = f"""
    Generate a list of {INDUSTRIES} random yet distinct and unique industries. Each industry should be a different industry that is commonly known.
    Put the industry in the 'industries' part of the JSON object, with the key for each being an incrementing int. The returned result will be a json object.

    The format of the json should be     
        ```json
    {{
        "industries": [
            "industry 1",
            "industry 2",
            ...
            "industry 5"
        ]
    }}
    ```
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': IndustryArray,
            },
        )
        data = response.parsed
        return data.industries
    except Exception as e:
        print(e)
        return "GEMINI AI RESPONSE FAILURE"

# Create a list of industries
# industries = gemini_create_industries()
# random.shuffle(industries)
# industries = industries[:5] # Limit to 15 industries

# Connect to SQLite database (creates the file if not exists)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create Industry table
cursor.execute("""
CREATE TABLE IF NOT EXISTS industry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT UNIQUE NOT NULL,
    industry_id INTEGER NOT NULL,
    starting_price REAL NOT NULL,
    employee_amt INTEGER NOT NULL,
    stock_name TEXT UNIQUE NOT NULL,
    FOREIGN KEY (industry_id) REFERENCES industry(id)
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS period_data (
    period_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    price REAL NOT NULL,
    next_price REAL NOT NULL,
    headline TEXT NOT NULL,
    details TEXT NOT NULL,
    public_approval INTEGER NOT NULL,
    technical_impact INTEGER NOT NULL,
    PRIMARY KEY (period_id, company_name)
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS comment (
    id INTEGER NOT NULL,
    headline_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    likes INTEGER NOT NULL,
    PRIMARY KEY (id, headline_id, comment),
    FOREIGN KEY (headline_id) REFERENCES headlines(id)
)
""")

conn.commit()


# Insert industries into the table
# cursor.executemany("INSERT OR IGNORE INTO industry (name) VALUES (?)", [(industry,) for industry in industries])

# Commit changes
# conn.commit()

# cursor.execute("SELECT id, name FROM industry")
# industry_data = {name: id for id, name in cursor.fetchall()}  # Dictionary mapping industry name to ID


cursor.execute("""
CREATE TABLE IF NOT EXISTS headlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_id INTEGER NOT NULL,
    headline TEXT UNIQUE NOT NULL,
    details TEXT NOT NULL,
    public_perception INTEGER NOT NULL,
    technical_impact INTEGER NOT NULL,
    FOREIGN KEY (industry_id) REFERENCES industry(id)
)""")

# for industry in industries:
#     industry_id = industry_data.get(industry)  # Get industry ID
#     headlines = gemini_create_prompts(industry)
#     for prompt in headlines:
#         details = gen_details(prompt)
#         (public_perception, technical_impact) = generate_trend(prompt)
#         cursor.execute("INSERT OR IGNORE INTO headlines (industry_id, headline, public_perception, technical_impact, details) VALUES (?, ?, ?, ?, ?)", (industry_id, prompt, public_perception, technical_impact, details))
#         conn.commit()
#         gen_extra_details(conn, prompt, public_perception)

# Commit changes and close the connectio
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS highscore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    top_score INTEGER NOT NULL,
    balance INTEGER NOT NULL
)
""")
conn.commit()

def gen_companies():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # SQL query to fetch 4 random industries
    cursor.execute("SELECT name FROM industry;")

    # Fetch results
    industries = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    for industry in industries:
        cursor.execute(""" SELECT id FROM industry WHERE name = ? """, (industry,))
        industry_id = cursor.fetchone()[0]
        if industry_id < 48:
            continue
        prompt = f"""
        Make a list of 4 random made-up companies (with one word names less than 30 characters). All 4 companies should be  in the industry of {industry}.
        Each company needs to have their stock market acronym, their respective stock costs, and the number of their employees.
        Then return the Companies with their Company name as the "name", their stock price as the "price", the number of employees as "employees", and their acronym as "stock_name" in a JSON object. The stock price is between 1 cent and 1000 dollars.
        """
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': GameStart,
                },
            )

            generated_text = response.text
            data = json.loads(generated_text)

            
            for company in data['companies']:
                cursor.execute("""
                INSERT OR IGNORE INTO company (company_name, starting_price, employee_amt, industry_id, starting_price, stock_name)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (company["name"], company["price"], company["employees"], industry_id, company["price"], company["stock_name"]))
            conn.commit()

        except Exception as e:
            raise "GEMINI AI RESPONSE FAILURE"
    return

gen_companies()


conn.close()

print(f"Database '{db_name}' created successfully with an table!")