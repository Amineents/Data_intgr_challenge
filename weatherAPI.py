from dotenv import load_dotenv
import requests
import json
import os

# Coordonnées
lat = 44.34
lon = 10.99

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")  



url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=fr"


folder_path = "data_like/bus"
os.makedirs(folder_path, exist_ok=True)  


file_path = os.path.join(folder_path, "weather_data.json")


response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Données météo sauvegardées dans '{file_path}'")
else:
    print(f"Erreur {response.status_code} : impossible de récupérer les données météo")
