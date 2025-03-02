import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Database file name
db_name = "small_db copy.db"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("""DELETE FROM industry WHERE id = 19 or id = 18 """,)
conn.commit()

conn.close()