from db_connect import get_db_connection
from db_connect import get_from_db

conn = get_db_connection()

rows = get_from_db(conn)
# print(len(rows))
for row in rows:
    (
        id,
        city,
        latitude,
        longitude,
        timestamp,
        date,
        time,
        temperature,
        feels_like,
        humidity,
        wind_speed,
        wind_direction,
    ) = row
    if city =='Hyderabad':
        print(f"{city}: {wind_speed} at {timestamp}")
