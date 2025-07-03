import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Détection du dossier data_lake/bus
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent
bus_dir = base_dir / "data_lake" / "bus"
bus_dir.mkdir(parents=True, exist_ok=True)

# Chemin du fichier de sortie
output_file = bus_dir / "trafic_routes_paris.csv"

# Liste des arrêts
bus_stops = [
    "Stade Charléty", "Gare Saint-Lazare", "Gare du Nord", "Porte d'Orléans",
    "Fort du Kremlin", "Châtelet", "Porte de la Muette", "Gare de Lyon",
    "Hôtel de Ville", "Parc de Saint-Cloud", "Luxembourg", "Neuilly",
    "Bastille", "Montparnasse", "Porte des Lilas", "Porte d’Ivry",
    "Champ de Mars", "Gambetta", "Pont Neuf", "École Militaire",
    "La Muette", "Opéra", "La Défense", "Musée d'Orsay",
    "Porte Maillot", "Gare de l'Est", "Bibliothèque F. Mitterrand"
]

# Génération de routes
routes = [(a, b) for a in bus_stops for b in bus_stops if a != b]

# Niveaux de trafic simulés
traffic_levels = ["léger", "modéré", "fort"]

# Nombre d'entrées à générer
num_entries = 300
start_time = datetime(2025, 1, 2, 6, 0, 0)  # cohérent avec les données météo

# Génération du fichier CSV
with output_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "route_from", "route_to", "traffic_level", "vehicle_count", "avg_speed_kmh", "timestamp"])
    
    for idx in range(1, num_entries + 1):
        frm, to = random.choice(routes)
        timestamp = (start_time + timedelta(minutes=idx)).strftime("%Y-%m-%d %H:%M:%S")
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
