import schedule
import time
import os
from dotenv import load_dotenv

from src.fetch import fetch_data
from src.db_connect import get_db_connection
from src.db_connect import insert_into_db
from src.transform import transform_record

import pandas as pd
import json 
import logging

def run_etl():
    # Your existing code goes here
    ...

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | Line:%(lineno)d | %(message)s",
    handlers=[
        logging.FileHandler(r"/logs/etl.log"),
        logging.StreamHandler()
    ]
)

# data_dump = []
with open(r'./data/cities.json','r') as f:
    cities = json.load(f)['cities']

# Connecting with DB
def run_etl():
    connection = None
    
    try:
        connection = get_db_connection()
        logging.info("Connection Established Succesfully")
        # iterating over cities defined in json to fetch their data
        for city in cities:
            lat = city["latitude"]
            lon = city["longitude"]
            URL = ( f"{os.getenv("API_BASE_URL")}?"
                f"latitude={lat}&longitude={lon}"
                    f"&current="
                        f"temperature_2m,"
                        f"relative_humidity_2m,"
                        f"apparent_temperature,"
                        f"precipitation,"
                        f"rain,"
                        f"surface_pressure,"
                        f"weather_code,"
                        f"wind_speed_10m,"
                        f"wind_direction_10m"
                        f"&timezone=Asia/Kolkata"

                    )
            try:
                raw_data = fetch_data(url=URL)
                logging.info(f'{city['city']}API data fetched succesfully')
                
                raw_data["city"] = city["city"]
                
                # extracting required fields from API res
                transformed_record = transform_record(raw_data)

                # save_json(transformed_record)
                # logging.info("Record Saved Successfully")
                
                # saving record into database
                # try:
                insert_into_db(conn=connection,record=transformed_record)
                
            except Exception as e:
                logging.error(f'Error {e}')
    
    # db connection error
    except Exception as e:
        logging.error(f'Connection Establishment Failed: {e}')
    
    # close db connection
    finally:
        if connection:
            connection.close()
                
                
schedule.every(3).minutes.do(run_etl)

# Run once immediately
run_etl()

logging.info("Scheduler started. Running every 3 minutes.")

while True:
    schedule.run_pending()
    time.sleep(1)