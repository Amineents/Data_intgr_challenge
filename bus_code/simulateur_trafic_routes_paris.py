import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

#  Dossier cible existant
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent 

bus_dir = base_dir / "data_lake" / "bus"
bus_dir.mkdir(parents=True, exist_ok=True)

# Fichier de sortie
output_file = bus_dir / "trafic_routes_paris.csv"




# Liste complète des arrêts
bus_stops = [
    "Stade Charléty", "Gare Saint-Lazare", "Gare du Nord", "Porte d'Orléans",
    "Fort du Kremlin", "Châtelet", "Porte de la Muette", "Gare de Lyon",
    "Hôtel de Ville", "Parc de Saint-Cloud", "Luxembourg", "Neuilly",
    "Bastille", "Montparnasse", "Porte des Lilas", "Porte d’Ivry",
    "Champ de Mars", "Gambetta", "Pont Neuf", "École Militaire",
    "La Muette", "Opéra", "La Défense", "Musée d'Orsay",
    "Porte Maillot", "Gare de l'Est", "Bibliothèque F. Mitterrand"
]

#  Paires de trajets possibles
routes = [(a, b) for a in bus_stops for b in bus_stops if a != b]

#  Paramètres de simulation
traffic_levels = ["léger", "modéré", "fort"]
num_entries = 100
start_time = datetime.now() - timedelta(hours=5)

#  Écriture du fichier CSV
with output_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "route_from", "route_to", "traffic_level", "vehicle_count", "avg_speed_kmh", "timestamp"])
    
    for idx in range(1, num_entries + 1):
        frm, to = random.choice(routes)
        timestamp = (start_time + timedelta(minutes=random.randint(0, 300))).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([
            idx,
            frm,
            to,
            random.choice(traffic_levels),
            random.randint(5, 150),
            round(random.uniform(10.0, 60.0), 1),
            timestamp
        ])

print(f" Fichier généré : {output_file}")
