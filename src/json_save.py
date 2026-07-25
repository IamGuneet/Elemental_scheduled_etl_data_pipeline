import json
import os

def save_json(chunk):
    filename = "data_dump.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    data.append(chunk)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)