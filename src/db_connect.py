import psycopg2
import logging
import os
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | Line:%(lineno)d | %(message)s",
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()
    ]
)

insert_query = """
INSERT INTO weather_data (
    city,
    latitude,
    longitude,
    timestamp,
    date,
    time,
    temperature,
    feels_like_temperature,
    relative_humidity,
    wind_speed,
    wind_direction
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

search_query = """
    SELECT * FROM weather_data 
"""


def get_db_connection(host=os.getenv("HOST"), database=os.getenv("DATABASE"), user=os.getenv("DATABASE"), password=os.getenv("PASSWORD"), port=os.getenv("PORT")):
    """
    Create and test a PostgreSQL database connection
    
    Args:
        host (str): Database host
        database (str): Database name
        user (str): Database user
        password (str): Database password
        port (int): Database port
    
    Returns:
        connection: PostgreSQL connection object if successful, None otherwise
    """
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cur = conn.cursor()
        
        cur.execute("SELECT version()")
        version = cur.fetchone()
        logging.info(f"Successfully connected to PostgreSQL!")
        print(f"Version: {version[0]}")
        
        cur.execute("SELECT datname FROM pg_database")
        databases = cur.fetchall()
        print(f"\nAvailable databases:")
        for db in databases:
            print(f"  - {db[0]}")
        
        cur.close()
        print("\nConnection test completed successfully!")
        return conn
        
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None
    
def insert_into_db(conn,record):
    try:
        curson = conn.cursor()
        curson.execute(insert_query,(
            record["city"],
            record["latitude"],
            record["longitude"],
            record["timestamp"],
            record["date"],
            record["time"],
            record["temperature"],
            record["feels_like_temperature"],
            record["relative_humidity"],
            record["wind_speed"],
            record["wind_direction"],
        ))
        logging.info("Record inserted successfully")
        
        conn.commit()
        curson.close()
    except Exception as e: 
        logging.error(f'ERROR SAVING RECORD {e}') 
        
def get_from_db(conn,query=search_query):
    try:
        curson = conn.cursor()
        curson.execute(query)
        output = curson.fetchall()
        logging.info("Record searched successfully")
        
        return output
    
    except Exception as e: 
        logging.error(f'ERROR SEARCHING RECORD {e}') 
    
    finally:
        if curson:
            curson.close()