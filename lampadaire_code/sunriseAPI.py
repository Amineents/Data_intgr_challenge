import requests
import json
import os

# Coordinates
lat = 44.138062
lng = 4.810250

# API endpoint
url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"


response = requests.get(url)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


folder_path = os.path.join(parent_dir, "data_lake", "lampadaires")
os.makedirs(folder_path, exist_ok=True)  


output_path = os.path.join(folder_path, "sunrise_sunset.json")


if response.status_code == 200:
    data = response.json()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to '{output_path}'")
else:
    print("Failed to fetch data:", response.status_code)
