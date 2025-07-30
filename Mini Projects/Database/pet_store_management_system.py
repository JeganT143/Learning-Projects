import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class PetStore:
    def __init__(self,host, database,user, port,password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection_params = {
            'host': self.host,
            'database': self.database,
            'port' : self.port,
            'user': self.user,
            'password': self.password
        }
    
    def connect(self):
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except Exception as e:
            print(f"Connection failed : {e}")
            return None
    
    def show_all_pets(self):
        conn = self.connect()
        if conn:
            query = """
            SELECT pet_id, name, species, magical_power, age, price,is_available
            FROM pets
            ORDER BY name;
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            print(df)
    
    def search_pets_by_price(self, max_price):
        conn = self.connect()
        if conn:
            query = """
            SELECT name, species, magical_power, price 
            FROM pets
            WHERE price <=%s AND is_available = TRUE
            ORDER BY price;
            """
            cursor = conn.cursor()
            cursor.execute(query,(max_price,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"\n Pets under ${max_price}: ")
            for pet in results:
                print(f"{pet[0]} the {pet[1]}  (${pet[3]} - {pet[2]})" )
                
    
    def adopt_pet(self, pet_id):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            
            # Check bet exists 
            query1 = """
            SELECT name, is_available FROM pets WHERE pet_id = %s
            """
            cursor.execute(query1, (pet_id,))
            result = cursor.fetchone()
            
            if result:
                name, is_available=result
                if is_available:
                    query2 = """
                    UPDATE pets SET is_available = FALSE
                    WHERE pet_id = %s
                    """
                    cursor.execute(query2, (pet_id,))
                    
                    conn.commit()
                    print(f"Addoptation Sucess for {name}")
                else:
                    print("Already adoped")
            else:
                print("Not Found")
            
            cursor.close()
            conn.close()


def main():
    host = os.getenv("PET_STORE_DB_HOST")
    database = os.getenv("PET_STORE_DB_DATABASE")
    user = os.getenv("PET_STORE_DB_USER")
    password=os.getenv("PET_STORE_DB_PASSWORD")
    port = os.getenv("PET_STORE_DB_PORT")
    
    store = PetStore(host,database,user,port,password)
    
    while True:
        print("1 => View all pets")
        print("2 => Search by price" )
        print("3 => Adopt a pet")
        print("4 => Exit")
        print()
        choice = input("Choose operation: 1 - 4 \n")
        print()
        if choice == "1":
            store.show_all_pets()
        elif choice == "2":
            try:
                butget = float(input("whats your budget ? "))
                store.search_pets_by_price(butget)
            except ValueError:
                print("Enter Valid Number : ")
        elif choice == "3":
            try : 
                pet_id = int(input("Enter Pet Id"))
                store.adopt_pet(pet_id)
            except ValueError:
                print("Enter Valid ID")
        elif choice == "4":
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()