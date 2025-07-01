import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

#  Création du dossier cible correct
landing_dir = Path("data_lake/landing/trafic_routes")
landing_dir.mkdir(parents=True, exist_ok=True)

#  Liste complète des arrêts officiels
bus_stops = [
    "Stade Charléty", "Gare Saint-Lazare", "Gare du Nord", "Porte d'Orléans",
    "Fort du Kremlin", "Châtelet", "Porte de la Muette", "Gare de Lyon",
    "Hôtel de Ville", "Parc de Saint-Cloud", "Luxembourg", "Neuilly",
    "Bastille", "Montparnasse", "Porte des Lilas", "Porte d’Ivry",
    "Champ de Mars", "Gambetta", "Pont Neuf", "École Militaire",
    "La Muette", "Opéra", "La Défense", "Musée d'Orsay",
    "Porte Maillot", "Gare de l'Est", "Bibliothèque F. Mitterrand"
]

#  Paires de routes entre arrêts distincts
routes = [
    (a, b) for a in bus_stops for b in bus_stops if a != b
]

#  Paramètres de simulation
traffic_levels = ["léger", "modéré", "fort"]
num_entries = 100
start_time = datetime.now() - timedelta(hours=5)

#  Génération des données
traffic_data = []
for _ in range(num_entries):
    frm, to = random.choice(routes)
    entry = {
        "timestamp": (start_time + timedelta(minutes=random.randint(0, 300))).isoformat(),
        "route_from": frm,
        "route_to": to,
        "traffic_level": random.choice(traffic_levels),
        "vehicle_count": random.randint(5, 150),
        "avg_speed_kmh": round(random.uniform(10.0, 60.0), 1)
    }
    traffic_data.append(entry)

# Écriture dans le fichier CSV final
output_file = landing_dir / "trafic_routes_paris.csv"
with output_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=traffic_data[0].keys())
    writer.writeheader()
    writer.writerows(traffic_data)

print(f" Fichier généré : {output_file}")
