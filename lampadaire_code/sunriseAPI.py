import requests
import json
import os

# Coordinates
lat = 44.138062
lng = 4.810250

# API endpoint
url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"


response = requests.get(url)


folder_path = "../data_like/lampadaires"
file_path = os.path.join(folder_path, "sunrise_sunset.json")


os.makedirs(folder_path, exist_ok=True)

if response.status_code == 200:
    data = response.json()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to '{file_path}'")
else:
    print("Failed to fetch data:", response.status_code)
