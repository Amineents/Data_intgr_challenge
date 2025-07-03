import mysql.connector

# Connexion à MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="amine",
    port=3306
)
cursor = conn.cursor()

# Création de la base Gold
cursor.execute("CREATE DATABASE IF NOT EXISTS golden_bus_lamp")
cursor.execute("USE golden_bus_lamp")

# 1. Vue retards enrichis avec météo
cursor.execute("""
CREATE OR REPLACE VIEW gold_bus_retards_enrichis AS
SELECT 
    r.ligne,
    r.gare_depart,
    r.gare_retard,
    r.heure_arrivee_prevue,
    r.heure_arrivee_reelle,
    l.position_gps,
    ROUND(w.temperature - 273.15, 2) AS temperature_celsius,
    w.humidity,
    w.wind_speed,
    w.cloud_percent,
    w.description AS meteo
FROM bus_silver.historique_retards r
JOIN bus_silver.localisation_bus l ON r.ligne = l.ligne
LEFT JOIN bus_silver.weather w ON DATE(r.heure_arrivee_prevue) = DATE(w.timestamp)
WHERE l.heure_de_captage IS NOT NULL;

""")


# 2. Vue retard moyen par ligne
cursor.execute("""
CREATE OR REPLACE VIEW gold_bus_retard_moyen_par_ligne AS
SELECT 
    ligne,
    AVG(TIMESTAMPDIFF(MINUTE, heure_arrivee_prevue, heure_arrivee_reelle)) AS retard_moyen,
    COUNT(*) AS nb_retards
FROM bus_silver.historique_retards
GROUP BY ligne
""")

# 3. Vue lampadaires défectueux
cursor.execute("""
CREATE OR REPLACE VIEW gold_lampadaires_defectueux AS
SELECT 
    r.lamp_id,
    s.etat_foy,
    s.marque,
    s.lon,
    s.lat,
    r.report_time,
    r.status
FROM lampadaires_silver.reclamations_lampadaires r
JOIN lampadaires_silver.lampadaires_static s ON r.lamp_id = s.lamp_id
""")

# 4. Vue consommation moyenne par lampe
cursor.execute("""
CREATE OR REPLACE VIEW gold_lampadaires_conso_moyenne AS
SELECT 
    c.lamp_id,
    AVG(c.consumption_kwh) AS conso_moyenne,
    MAX(c.ts) AS derniere_mesure
FROM lampadaires_silver.consommation_lampadaires c
GROUP BY c.lamp_id
""")

# 5. Vue allumage vs coucher de soleil
cursor.execute("""
CREATE OR REPLACE VIEW gold_allumage_vs_sunset AS
SELECT 
    p.lamp_id,
    p.date,
    p.on_time,
    p.off_time,
    s.sunset,
    s.sunrise
FROM lampadaires_silver.planning_allumage p
CROSS JOIN lampadaires_silver.sunrise_sunset s
""")

conn.commit()
cursor.close()
conn.close()

print("Golden views créées avec succès dans la base 'golden_bus_lamp'.")
