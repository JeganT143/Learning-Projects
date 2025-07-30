import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

# Load environvariables 
host = os.getenv("PET_STORE_DB_HOST")
database = os.getenv("PET_STORE_DB_DATABASE")
user = os.getenv("PET_STORE_DB_USER")
password=os.getenv("PET_STORE_DB_PASSWORD")
port = os.getenv("PET_STORE_DB_PORT")

# Connection details
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host= host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Connection Success")
        return connection
    except Exception as e:
        print(f"Error connecting to database : {e}")
        return None

# Function to get all pets
def get_all_pets():
    conn = connect_to_db()
    if conn:
        query = "SELECT * FROM pets"
        df = pd.read_sql_query(query, conn),
        conn.close()
        return df
    return None

# Function to add a new pet
def add_new_pet(name, species, magical_power, age, price):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO pets (name, species, magical_power, age, price)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, species, magical_power, age, price))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Added {name} the {species} to the DB")

# add_new_pet("broody","dog","24*7 sleep", 2, 50000)
print(get_all_pets())