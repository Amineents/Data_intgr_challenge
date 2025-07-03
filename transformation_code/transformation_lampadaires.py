
import pandas as pd
import mysql.connector
import json
import os

# Détection des chemins dynamiques
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data_lake", "lampadaires")

# Connexion à MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="my-secret-pw",
    port=3306,
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS lampadaires_silver")
cursor.execute("USE lampadaires_silver")

# --- 1. lampadaires_datasud.csv ---
df_static = pd.read_csv(os.path.join(data_dir, "lampadaires_datasud.csv"), sep=";")
df_static.columns = [col.strip().lower().replace(" ", "_") for col in df_static.columns]

# Création de lamp_id à partir de gid
df_static["lamp_id"] = df_static["gid"].apply(lambda x: f"LAMP{int(x):05}")

# Colonnes d'intérêt dans l'ordre donné
df_static = df_static[[
    "lamp_id",
    "marque",
    "etat_foy",
    "type_amp",
    "plamp",
    "etat_cro",
    "vasque",
    "lon",
    "lat"
]]

df_static["lon"] = pd.to_numeric(df_static["lon"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
df_static["lat"] = pd.to_numeric(df_static["lat"].astype(str).str.replace(",", ".", regex=False), errors="coerce")

df_static.drop_duplicates(inplace=True)
assert df_static["lamp_id"].is_unique, "ID en double dans lampadaires_datasud.csv"

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS lampadaires_static (
    lamp_id VARCHAR(50) PRIMARY KEY,
    marque VARCHAR(100),
    etat_foy VARCHAR(100),
    type_amp VARCHAR(100),
    plamp VARCHAR(100),
    etat_cro VARCHAR(100),
    vasque VARCHAR(100),
    lon FLOAT,
    lat FLOAT
)
""")

for _, row in df_static.iterrows():
    cursor.execute("""
        INSERT INTO lampadaires_static (
            lamp_id, marque, etat_foy, type_amp, plamp, etat_cro, vasque, lon, lat
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(None if pd.isna(v) else v for v in row))




# --- 2. lampadaires_streaming_simulation.jsonl ---
df_stream = pd.read_json(os.path.join(data_dir, "lampadaires_streaming_simulation.jsonl"), lines=True)
df_stream.columns = [col.strip().lower() for col in df_stream.columns]
df_stream["lamp_id"] = df_stream["lamp_id"].str.strip().str.upper()
df_stream["ts"] = pd.to_datetime(df_stream["ts"])
df_stream.drop_duplicates(inplace=True)

cursor.execute("""
CREATE TABLE IF NOT EXISTS consommation_lampadaires (
    lamp_id VARCHAR(50),
    ts DATETIME,
    consumption_kwh FLOAT
)
""")
for _, row in df_stream.iterrows():
    cursor.execute("""
        INSERT INTO consommation_lampadaires (lamp_id, ts, consumption_kwh)
        VALUES (%s, %s, %s)
    """, tuple(row))

# --- 3. planning_allumage_saisonnier.csv ---
df_plan = pd.read_csv(os.path.join(data_dir, "planning_allumage_saisonnier.csv"))
df_plan.columns = [col.strip().lower() for col in df_plan.columns]
df_plan["lamp_id"] = df_plan["lamp_id"].str.upper().str.strip()
df_plan.drop_duplicates(inplace=True)

cursor.execute("""
CREATE TABLE IF NOT EXISTS planning_allumage (
    lamp_id VARCHAR(50),
    date DATE,
    on_time TIME,
    off_time TIME
)
""")
for _, row in df_plan.iterrows():
    cursor.execute("""
        INSERT INTO planning_allumage (lamp_id, date, on_time, off_time)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

# --- 4. reclamations_lampadaires.jsonl ---
df_reclam = pd.read_json(os.path.join(data_dir, "reclamations_lampadaires.jsonl"), lines=True)
df_reclam.columns = [col.strip().lower() for col in df_reclam.columns]
df_reclam["lamp_id"] = df_reclam["lamp_id"].str.upper().str.strip()
df_reclam["report_time"] = pd.to_datetime(df_reclam["report_time"])
df_reclam["status"] = df_reclam["status"].str.lower().str.strip()
df_reclam.drop_duplicates(inplace=True)

cursor.execute("""
CREATE TABLE IF NOT EXISTS reclamations_lampadaires (
    lamp_id VARCHAR(50),
    report_time DATETIME,
    status VARCHAR(50)
)
""")
for _, row in df_reclam.iterrows():
    cursor.execute("""
        INSERT INTO reclamations_lampadaires (lamp_id, report_time, status)
        VALUES (%s, %s, %s)
    """, tuple(row))

# --- 5. sunrise_sunset.json ---
with open(os.path.join(data_dir, "sunrise_sunset.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

sunrise = data.get("results", {}).get("sunrise")
sunset = data.get("results", {}).get("sunset")
day_length = data.get("results", {}).get("day_length")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sunrise_sunset (
    sunrise VARCHAR(50),
    sunset VARCHAR(50),
    day_length VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
    INSERT INTO sunrise_sunset (sunrise, sunset, day_length)
    VALUES (%s, %s, %s)
""", (sunrise, sunset, day_length))

conn.commit()
cursor.close()
conn.close()

print("Données lampadaires nettoyées, transformées et insérées dans 'lampadaires_silver'.")
