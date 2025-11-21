import psycopg2
from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()
psql_password = os.getenv("PSQL_PASSWORD") #Update your .env file with PSQL_PASSWORD=insert_password_here

connection = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=psql_password,
    port=5432
)

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS webUser (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    email TEXT,
    is_verified_human TEXT
);
""")

connection.commit()

cursor.close()
connection.close()