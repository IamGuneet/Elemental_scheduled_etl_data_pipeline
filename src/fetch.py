import requests

def fetch_data(url:str):
    if not url:
        raise ValueError("URL Cannot be empty")
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data from API:{e}")
