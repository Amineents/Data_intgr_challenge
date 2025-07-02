import os
import pandas as pd
import mysql.connector
import json
from datetime import datetime
from pathlib import Path

# Connexion à MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="amine",
    port=3306
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bus_silver")
cursor.execute("USE bus_silver")

# Détection dynamique du dossier data_lake
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_path = Path(parent_dir) / "data_lake" / "bus"

# === 1. localisation_bus_paris.csv ===
df_loc = pd.read_csv(data_path / "localisation_bus_paris.csv")
df_loc.columns = [col.strip().lower().replace(" ", "_") for col in df_loc.columns]
df_loc['ligne'] = df_loc['ligne'].astype(str).str.upper().str.strip()
df_loc['gare_depart'] = df_loc['gare_depart'].astype(str).str.title().str.strip()
df_loc['destination'] = df_loc['destination'].astype(str).str.title().str.strip()
df_loc.drop_duplicates(inplace=True)
assert df_loc['id'].is_unique, "ID en double dans localisation_bus"

cursor.execute("""
    CREATE TABLE IF NOT EXISTS localisation_bus (
        id INT PRIMARY KEY,
        ligne VARCHAR(10),
        gare_depart VARCHAR(100),
        destination VARCHAR(100),
        position_gps VARCHAR(50),
        heure_de_captage DATETIME
    )
""")
for _, row in df_loc.iterrows():
    cursor.execute("""
        INSERT INTO localisation_bus (id, ligne, gare_depart, destination, position_gps, heure_de_captage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

# === 2. trafic_routes_paris.csv ===
df_traf = pd.read_csv(data_path / "trafic_routes_paris.csv")
df_traf.columns = ["id", "route_from", "route_to", "traffic_level", "vehicle_count", "avg_speed_kmh", "timestamp"]

# Nettoyage
df_traf['route_from'] = df_traf['route_from'].astype(str).str.title().str.strip()
df_traf['route_to'] = df_traf['route_to'].astype(str).str.title().str.strip()
df_traf['traffic_level'] = df_traf['traffic_level'].astype(str).str.lower().str.strip()
df_traf['timestamp'] = pd.to_datetime(df_traf['timestamp'], errors='coerce')

# Nettoyage des erreurs et doublons
df_traf.dropna(subset=["timestamp"], inplace=True)
df_traf.drop_duplicates(inplace=True)

# Vérification des points manquants
points_connus = set(df_loc['gare_depart'].dropna().unique()) | set(df_loc['destination'].dropna().unique())
points_trafic = set(df_traf['route_from'].dropna().unique()) | set(df_traf['route_to'].dropna().unique())
points_manquants = points_trafic - points_connus
if points_manquants:
    print("Points de trafic non référencés dans les gares :", points_manquants)

# Création de la table
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

# Insertion
for _, row in df_traf.iterrows():
    cursor.execute("""
        INSERT INTO trafic_routes (
            id, route_from, route_to, traffic_level, vehicle_count, avg_speed_kmh, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))


# === 3. historique_retards.csv ===
df_retards = pd.read_csv(data_path / "historique_retards.csv")
df_retards.columns = [col.strip().lower().replace(" ", "_") for col in df_retards.columns]

# Vérification et nettoyage
df_retards['ligne'] = df_retards['ligne'].astype(str).str.upper().str.strip()
df_retards['gare_depart'] = df_retards['gare_depart'].astype(str).str.title().str.strip()
df_retards['gare_retard'] = df_retards['gare_retard'].astype(str).str.title().str.strip()
df_retards['heure_arrivee_prevue'] = pd.to_datetime(df_retards['heure_arrivee_prevue'], errors='coerce')
df_retards['heure_arrivee_reelle'] = pd.to_datetime(df_retards['heure_arrivee_reelle'], errors='coerce')
df_retards.drop_duplicates(inplace=True)

# Table simplifiée : on conserve les colonnes du fichier
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historique_retards (
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
        INSERT INTO historique_retards (id_bus, ligne, gare_depart, gare_retard, heure_arrivee_prevue, heure_arrivee_reelle)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))


# === 4. horaires_arrets_bus.csv ===
df_horaires = pd.read_csv(data_path / "horaires_arrets_bus.csv")
df_horaires.columns = ["ligne", "nom_arret", "placement_gare", "heure_passage", "ordre_arret"]
df_horaires['nom_arret'] = df_horaires['nom_arret'].astype(str).str.title().str.strip()
df_horaires['placement_gare'] = df_horaires['placement_gare'].astype(str).str.strip()
df_horaires.drop_duplicates(inplace=True)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS horaires_arrets (
        ligne VARCHAR(10),
        nom_arret VARCHAR(100),
        placement_gare VARCHAR(100),
        heure_passage DATETIME,
        ordre_arret INT
    )
""")
for _, row in df_horaires.iterrows():
    cursor.execute("""
        INSERT INTO horaires_arrets (ligne, nom_arret, placement_gare, heure_passage, ordre_arret)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))

# === 5. weather_data.json ===
with open(data_path / "weather_data.json", "r", encoding="utf-8") as f:
    weather_json = json.load(f)

# Création de la table (inchangé)
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

# Insertion de chaque entrée dans la liste
for entry in weather_json.get("list", []):
    timestamp = datetime.fromtimestamp(entry["dt"])
    temp = entry["main"]["temp"]
    humidity = entry["main"]["humidity"]
    wind_speed = entry["wind"]["speed"]
    rain = entry.get("rain", {}).get("1h", 0)
    clouds = entry["clouds"]["all"]
    description = entry["weather"][0]["description"]
    
    # city name fallback
    city = weather_json.get("city", {}).get("name", "Paris")

    cursor.execute("""
        INSERT INTO weather (city_name, temperature, humidity, wind_speed, rain_1h, cloud_percent, description, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (city, temp, humidity, wind_speed, rain, clouds, description, timestamp))


# Fin
conn.commit()
cursor.close()
conn.close()

print("Données des bus nettoyées, cohérentes, transformées et insérées dans 'bus_silver'.")
