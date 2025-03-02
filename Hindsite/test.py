from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import sqlite3
import random
import time
from datetime import datetime
from stock_data import get_stock_trends

# Load environment variables from .env file
load_dotenv()
db_name = "small_db.db"
backup_file = "backup.txt"
connx = None

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

class Headline(BaseModel):
    title: str
    detail: str

class Comment(BaseModel):
    comment: str
    likes: int

class Details(BaseModel):
    details: str

def gen_details(headline):
    prompt = f"""
    Given the company and the present headline:
    - CURRENT HEADLINE: {headline}
    Any place the company name needs to be placed, replace with "{{name}}" as a placeholder.
    Based upon the company's current headline, pretend to be the reporter writing the article about the current headline. Write two sentences giving details about the headline. You are not allowed to discuss anything involving the stock market, or how any action will impact the stock market.
    In the JSON, the details will be the 'details' part of the JSON object. Return this in a JSON object.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': Details,
            },
        )
        details = response.parsed
        return details.details
    except Exception as e:
        with open(backup_file, "w") as f:
            for line in connx.iterdump():
                f.write(f"{line}\n")

        return "GEMINI AI RESPONSE FAILURE"


# Generate AI headlines for company stories
def generate_data(company_name):
    global connx
    conn = sqlite3.connect(db_name)
    connx = conn
    cursor = conn.cursor()

    # SQL query to fetch 4 random industries
    cursor.execute("SELECT headline FROM headlines ORDER BY RANDOM() LIMIT 1;")
    
    # Fetch results
    data = cursor.fetchone()
    rand_headline = data[0]
    
    # Close the database connection
    conn.close()

    prompt = f"""
    Given the company and the present headline:
    - Company name: {company_name}
    - CURRENT HEADLINE: {rand_headline}

    Based upon the company's current headline, pretend to be the reporter writing the article about the current headline. Write two sentences giving details about the headline. You are not allowed to discuss anything involving the stock market, or how any action will impact the stock market.
    The company may have previous headlines, (assume each of the previous headlines was made 6 months apart from eachother).
    In the JSON, the headline will be the 'title' part of the JSON object, and any added details will be the 'details'. Return this in a JSON object.
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
        with open(backup_file, "w") as f:
            # Use .dump to write database contents to file
            for line in connx.iterdump():
                f.write(f"{line}\n")

        headline = "GEMINI AI RESPONSE FAILURE"
        return headline, [], 0, 0

    (public_perception, technical_impact) = generate_trend(headline)

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

    Do NOT include anything except the JSON response. No explanations or extra text.
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
        print(e)
        with open(backup_file, "w") as f:
            # Use .dump to write database contents to file
            global connx
            for line in connx.iterdump():
                f.write(f"{line}\n")

        comment = None
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

    Do NOT include anything except the JSON response. No explanations or extra text.
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
        with open(backup_file, "w") as f:
            # Use .dump to write database contents to file
            global connx
            for line in connx.iterdump():
                f.write(f"{line}\n")

        print(e)
        comment = None
    return comment


def generate_trend(data):
    public_perception = 0
    technical_impact = 0
    time.sleep(8)
    prompt = f"""
    Given the following headline JSON object:
    - HEADLINE: ${data}

    Based on the headline and the way it describes the company's changes and possible problems, 
    generate two constants that describe the public's perception of the company(1-20, 1 being most negative response to the headline, 20 being most positive response to the headline).
    and the actual impact the news described in the headline may actually have on the functionality of the company
    from a technical standpoint (1-20, 1 being most negative impact to the company, 20 being most positive). Please just only give the two numbers, nothing else as a response, with the public perception first and the technical impact second. Formatted like i,j just being separated by a comma. 
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
        with open(backup_file, "w") as f:
            # Use .dump to write database contents to file
            global connx
            for line in connx.iterdump():
                f.write(f"{line}\n")

        print("GEMINI AI RESPONSE FAILURE")
        raise e

class CompanyFull(BaseModel):
    name: str
    price: float
    employees: int
    stock_name: str

class GameStart(BaseModel):
    companies: list[CompanyFull]

def getPeriodData(per_dat, price):
    res = dict()
    for i in range(1, 11):
        p = price
        res[i] = dict()
        a, b = stock_data(p, per_dat["public_perception"], per_dat["technical_impact"])
        res[i]["next_price"] = b
        res[i]["datapoint1"] = a[0]
        res[i]["datapoint2"] = a[1]
        res[i]["datapoint3"] = a[2]
        res[i]["datapoint4"] = a[3]
        res[i]["datapoint5"] = a[4]
        res[i]["datapoint6"] = a[5]
        res[i]["datapoint7"] = a[6]
        res[i]["datapoint8"] = a[7]
        res[i]["datapoint9"] = a[8]
        res[i]["datapoint10"] = a[9]
        p = b
    return res
    

def game_start_gen():
    periods = dict()
    stocks = dict()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # SQL query to fetch 4 random industries
    cursor.execute("SELECT id FROM industry ORDER BY RANDOM() LIMIT 4;")

    industries = cursor.fetchall()

    industry_map = {row[0]: idx for idx, row in enumerate(industries)}

    # Select 4 unique industries
    random_selection = random.sample(list(industry_map.keys()), 4)

    for index, industry_id in enumerate(random_selection):
        limit = 3 if index in [0, 2] else 2
        cursor.execute("""
            SELECT company_name, starting_price, employee_amt, stock_name
            FROM company 
            WHERE industry_id = ? 
            ORDER BY RANDOM() 
            LIMIT ?;
        """, (industry_id, limit))

        # Fetch companies
        companies = cursor.fetchall()
        
        cursor.execute("""
        SELECT headline, details, public_perception, technical_impact, id FROM headlines WHERE industry_id = ? ORDER BY RANDOM() LIMIT ?
        """, (industry_id, 10*limit,))
        per_dat = cursor.fetchall()

        # Store in dictionary
        x = 0
        for company in companies:
            stocks[company[0]] = {
                "start_price": company[1],
                "emp_amt": company[2],
                "industry": industry_map[industry_id],
                "acronym": company[3]
            }
            price = company[1]
            for i in range(1, 11):
                data = getPeriodData(per_dat[x], price)
                cursor.execute("""
                SELECT comment, likes FROM comment WHERE headline_id = ?
                """, (per_dat[x][4],))
                comments = cursor.fetchall()

                periods[i][company[0]] = {
                    "curr_price": price,
                    "next_price": data[i]["next_price"],
                    "headline": per_dat[x*i + i][0],
                    "detail": per_dat[x*i + i][1],
                    "comments": { "1": {"comment": comments[0]["comment"], "likes": comments[0]["likes"]}, 
                                  "2": {"comment": comments[1]["comment"], "likes": comments[1]["likes"]},
                                  "3": {"comment": comments[2]["comment"], "likes": comments[2]["likes"]}, 
                                },
                    "datapoints": {
                                    "1": data[i]["datapoint1"],
                                    "2": data[i]["datapoint2"],
                                    "3": data[i]["datapoint3"],
                                    "4": data[i]["datapoint4"],
                                    "5": data[i]["datapoint5"],
                                    "6": data[i]["datapoint6"],
                                    "7": data[i]["datapoint7"],
                                    "8": data[i]["datapoint8"],
                                    "9": data[i]["datapoint9"],
                                    "10": data[i]["datapoint10"]
                    }
                }
                price = data[i]["next_price"]
            x += 1
            

    # Close the database connection
    conn.close()

    return periods, stocks


# comp_dat = {"price": 192, "industry": "Military", "employees": 342, "history": {}}


# company_n = "Appian Technologies"
# current_time = datetime.now().strftime("%H:%M:%S")
# print("Current Time:", current_time)
# result = generate_data(comp_dat, company_n)
# # current_time = datetime.now().strftime("%H:%M:%S")
# # print("Current Time:", current_time)
# print(result)

# print(len(result))
# for headline, com, public_perception, technical_impact in result:
#     print(f"\nHEADLINE: {headline.title}\nDETAILS: {headline.detail}\n")

#     print("COMMENTS:")
    # for commment in com:
    #     print(f"\t{commment.likes} likes: {commment.comment}\n\n")



def gen_companies():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # SQL query to fetch 4 random industries
    cursor.execute("SELECT name FROM industry;")

    # Fetch results
    industries = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()
    for industry in industries:
        prompt = f"""
        Make a list of ten random made-up companies (with one word names less than 30 characters). All 10 companies should be  in the industry of {random_industries[0]}.
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

            cursor.execute(""" SELECT id FROM industry WHERE industry_name = ? """, (company.industry,))
            industry_id = cursor.fetchone()[0]

            cursor.execute("""
            INSERT INTO company (company_name, employee_amt, industry_id, starting_price)
            VALUES (?, ?, ?, ?)
            """, (company.name, company.price, company.employees, industry_id, company.price))
            conn.commit()

            return

        except Exception as e:
            raise "GEMINI AI RESPONSE FAILURE"




# Populate the database
def populate_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    gen_companies()

    cursor.execute("SELECT company_name, industry_id FROM company")
    companies = cursor.fetchall()
    for i in range(1, 11): # 1 to 10
        for company_name, industry_id in companies:
            if i == 1:
                cursor.execute("""SELECT starting_price FROM company WHERE company_name = ?""", (company_name,))
            else:
                cursor.execute("""SELECT next_price FROM period_data WHERE company_name = ? and period = ?""", (company_name, i - 1))
            cur_price = cursor.fetchone()[0]

            # Generate company news & stock trends
            headline, comments, public_perception, technical_impact = generate_data(company_name)
            stock_data, final_price = get_stock_trends(cur_price, public_perception, technical_impact)

            # Insert into period_data
            cursor.execute("""
            INSERT INTO period_data (period_id, company_name, price, next_price, headline, details, public_approval, technical_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (i, company_name, cur_price, final_price, headline.title, headline.detail, public_perception, technical_impact))

            conn.commit()

            # Insert stock trend points
            for offset, y_val in stock_data.items():
                cursor.execute("""
                INSERT INTO period_point (period_id, company_name, offset, y_val)
                VALUES (?, ?, ?, ?)
                """, (i, company_name, offset + 1, y_val))
            conn.commit()


            # Insert comments
            for comment in comments:
                cursor.execute("""
                INSERT INTO comment (period_id, company_name, comment, likes)
                VALUES (?, ?, ?, ?)
                """, (i, company_name, comment.comment, comment.likes))
            conn.commit()

    conn.commit()
    conn.close()
