import logging
from datetime import datetime

def transform_record(record):
# extracting relevant field from api response
    try:
        city = record['city']
        latitude = record['latitude']
        longitude = record['longitude']
        time = record['current']['time']
        # extracting date and time from iso format
        dt = datetime.fromisoformat(time)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        
        temperature = record['current']['temperature_2m']
        feels_like_temperature = record['current']['apparent_temperature']
        relative_humidity_2m = record['current']['relative_humidity_2m']
        wind_speed = record['current']['wind_speed_10m']
        wind_direction = record['current']['wind_direction_10m']
        
        logging.info("Record Fileds Extracted Succefulyy")
        return {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp":dt.isoformat(sep=" "),
            "date": date_str,
            "time": time_str,
            "temperature": temperature,
            "feels_like_temperature": feels_like_temperature,
            "relative_humidity": relative_humidity_2m,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction
        }
        
    except Exception as e:
        logging.error(f'Missing field: {e}')
        return None     
    




































