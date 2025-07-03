import os
import pandas as pd
import mysql.connector
import json
from datetime import datetime
from pathlib import Path

# Détection dynamique du dossier data_lake
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_path = Path(parent_dir) / "data_lake" / "bus"
print(data_path)

# Connexion à la base bus_silver
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="my-secret-pw",
    port=3306,
    database="bus_silver"
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bus_silver")
cursor.execute("USE bus_silver")

# === 1. localisation_bus_paris.csv ===
df_loc = pd.read_csv(data_path / "localisation_bus_paris.csv")
df_loc.columns = [col.strip().lower().replace(" ", "_") for col in df_loc.columns]
df_loc['ligne'] = df_loc['ligne'].astype(str).str.upper().str.strip()
df_loc['gare_depart'] = df_loc['gare_depart'].astype(str).str.title().str.strip()
df_loc['destination'] = df_loc['destination'].astype(str).str.title().str.strip()

# 🔁 Conversion correcte des dates
df_loc['heure_de_captage'] = pd.to_datetime(df_loc['heure_de_captage'], format="%d/%m/%Y %H:%M", errors='coerce')

df_loc.dropna(subset=["heure_de_captage"], inplace=True)
df_loc.drop_duplicates(inplace=True)

# Ajout de la colonne id_localisation
df_loc.insert(0, "id_localisation", range(1, len(df_loc) + 1))

cursor.execute("""
    CREATE TABLE IF NOT EXISTS localisation_bus (
        id_localisation INT PRIMARY KEY,
        ligne VARCHAR(10),
        gare_depart VARCHAR(100),
        destination VARCHAR(100),
        position_gps VARCHAR(50),
        heure_de_captage DATETIME
    )
""")
for _, row in df_loc.iterrows():
    cursor.execute("""
        INSERT INTO localisation_bus (id_localisation, ligne, gare_depart, destination, position_gps, heure_de_captage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        int(row['id_localisation']),
        row['ligne'],
        row['gare_depart'],
        row['destination'],
        row['position_gps'],
        row['heure_de_captage'].strftime("%Y-%m-%d %H:%M:%S")
    ))

# === 2. trafic_routes_paris.csv ===
df_traf = pd.read_csv(data_path / "trafic_routes_paris.csv")
df_traf.columns = ["id", "route_from", "route_to", "traffic_level", "vehicle_count", "avg_speed_kmh", "timestamp"]
df_traf['route_from'] = df_traf['route_from'].astype(str).str.title().str.strip()
df_traf['route_to'] = df_traf['route_to'].astype(str).str.title().str.strip()
df_traf['traffic_level'] = df_traf['traffic_level'].astype(str).str.lower().str.strip()
df_traf['timestamp'] = pd.to_datetime(df_traf['timestamp'], errors='coerce')
df_traf.dropna(subset=["timestamp"], inplace=True)
df_traf.drop_duplicates(inplace=True)

points_connus = set(df_loc['gare_depart'].dropna().unique()) | set(df_loc['destination'].dropna().unique())
points_trafic = set(df_traf['route_from'].dropna().unique()) | set(df_traf['route_to'].dropna().unique())
points_manquants = points_trafic - points_connus
if points_manquants:
    print("Points de trafic non référencés dans les gares :", points_manquants)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS trafic_routes (
        id INT PRIMARY KEY,
        route_from VARCHAR(100),
        route_to VARCHAR(100),
        traffic_level VARCHAR(20),
        vehicle_count INT,
        avg_speed_kmh FLOAT,
        timestamp DATETIME
    )
""")
for _, row in df_traf.iterrows():
    cursor.execute("""
        INSERT INTO trafic_routes (
            id, route_from, route_to, traffic_level, vehicle_count, avg_speed_kmh, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row['id']),
        row['route_from'],
        row['route_to'],
        row['traffic_level'],
        int(row['vehicle_count']),
        float(row['avg_speed_kmh']),
        row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    ))

# === 3. historique_retards.csv ===
df_retards = pd.read_csv(data_path / "historique_retards.csv")
df_retards.columns = [col.strip().lower().replace(" ", "_") for col in df_retards.columns]
df_retards['ligne'] = df_retards['ligne'].astype(str).str.upper().str.strip()
df_retards['gare_depart'] = df_retards['gare_depart'].astype(str).str.title().str.strip()
df_retards['gare_retard'] = df_retards['gare_retard'].astype(str).str.title().str.strip()
df_retards['heure_arrivee_prevue'] = pd.to_datetime(df_retards['heure_arrivee_prevue'], errors='coerce')
df_retards['heure_arrivee_reelle'] = pd.to_datetime(df_retards['heure_arrivee_reelle'], errors='coerce')
df_retards.drop_duplicates(inplace=True)

df_retards.insert(0, "id_retard", range(1, len(df_retards) + 1))

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historique_retards (
        id_retard INT PRIMARY KEY,
        id_bus INT,
        ligne VARCHAR(10),
        gare_depart VARCHAR(100),
        gare_retard VARCHAR(100),
        heure_arrivee_prevue DATETIME,
        heure_arrivee_reelle DATETIME
    )
""")
for _, row in df_retards.iterrows():
    cursor.execute("""
        INSERT INTO historique_retards (
            id_retard, id_bus, ligne, gare_depart, gare_retard, heure_arrivee_prevue, heure_arrivee_reelle
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# === 4. horaires_arrets_bus.csv ===
df_horaires = pd.read_csv(data_path / "horaires_arrets_bus.csv")
df_horaires.columns = ["ligne", "nom_arret", "placement_gare", "heure_passage", "ordre_arret"]
df_horaires['nom_arret'] = df_horaires['nom_arret'].astype(str).str.title().str.strip()
df_horaires['placement_gare'] = df_horaires['placement_gare'].astype(str).str.strip()
df_horaires['heure_passage'] = pd.to_datetime(df_horaires['heure_passage'], errors='coerce')
df_horaires.drop_duplicates(inplace=True)
df_horaires.insert(0, "id_horaires", range(1, len(df_horaires) + 1))

cursor.execute("""
    CREATE TABLE IF NOT EXISTS horaires_arrets (
        id_horaires INT PRIMARY KEY,
        ligne VARCHAR(10),
        nom_arret VARCHAR(100),
        placement_gare VARCHAR(100),
        heure_passage DATETIME,
        ordre_arret INT
    )
""")
for _, row in df_horaires.iterrows():
    cursor.execute("""
        INSERT INTO horaires_arrets (
            id_horaires, ligne, nom_arret, placement_gare, heure_passage, ordre_arret
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

# === 5. weather_data.json ===
with open(data_path / "weather_data.json", "r", encoding="utf-8") as f:
    weather_json = json.load(f)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        city_name VARCHAR(100),
        temperature FLOAT,
        humidity INT,
        wind_speed FLOAT,
        rain_1h FLOAT,
        cloud_percent INT,
        description VARCHAR(100),
        timestamp DATETIME
    )
""")
for entry in weather_json.get("list", []):
    timestamp = datetime.fromtimestamp(entry["dt"])
    temp = entry["main"]["temp"]
    humidity = entry["main"]["humidity"]
    wind_speed = entry["wind"]["speed"]
    rain = entry.get("rain", {}).get("1h", 0)
    clouds = entry["clouds"]["all"]
    description = entry["weather"][0]["description"]
    city = weather_json.get("city", {}).get("name", "Paris")

    cursor.execute("""
        INSERT INTO weather (city_name, temperature, humidity, wind_speed, rain_1h, cloud_percent, description, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (city, temp, humidity, wind_speed, rain, clouds, description, timestamp.strftime("%Y-%m-%d %H:%M:%S")))

# Affichage des tables créées
cursor.execute("SHOW TABLES;")
for table in cursor:
    print(table)

conn.commit()
cursor.close()
conn.close()

print("✅ Données transformées avec succès et insérées dans 'bus_silver'.")
