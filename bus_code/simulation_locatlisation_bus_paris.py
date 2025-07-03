import csv
from datetime import datetime, timedelta
import random
import os

ares_par_ligne = {
    "21": ["Stade Charléty", "Alésia", "Denfert-Rochereau", "Montparnasse", "Opéra", "Gare Saint-Lazare"],
    "38": ["Gare du Nord", "Châtelet", "Luxembourg", "Raspail", "Alésia", "Porte d'Orléans"],
    "47": ["Fort du Kremlin", "Ivry", "Place d'Italie", "Gare d'Austerlitz", "Hôtel de Ville", "Châtelet"],
    "63": ["Porte de la Muette", "La Muette", "Trocadéro", "Invalides", "Gare d'Austerlitz", "Gare de Lyon"],
    "72": ["Hôtel de Ville", "Concorde", "Pont de l'Alma", "Musée du quai Branly", "Pont Mirabeau", "Parc de Saint-Cloud"],
    "82": ["Luxembourg", "Montparnasse", "Invalides", "Charles de Gaulle Étoile", "Bois de Boulogne", "Neuilly"],
    "91": ["Bastille", "Gare de Lyon", "Place d'Italie", "Raspail", "Gare Montparnasse", "Montparnasse"],
    "96": ["Gare Montparnasse", "Odéon", "Hôtel de Ville", "République", "Ménilmontant", "Porte des Lilas"],
    "27": ["Gare Saint-Lazare", "Opéra", "Châtelet", "Gare d'Austerlitz", "Bibliothèque", "Porte d’Ivry"],
    "69": ["Champ de Mars", "Invalides", "Louvre", "Bastille", "Père Lachaise", "Gambetta"],
    "24": ["Pont Neuf", "Châtelet", "Odéon", "Invalides", "École Militaire"],
    "52": ["La Muette", "Trocadéro", "Champs-Élysées", "Madeleine", "Opéra"],
    "73": ["La Défense", "Neuilly", "Porte Maillot", "Concorde", "Musée d'Orsay"],
    "30": ["Porte Maillot", "Ternes", "Place de Clichy", "Gare du Nord", "Gare de l'Est"],
    "87": ["Gare de Lyon", "Bibliothèque F. Mitterrand"]
}

# Déterminer dynamiquement le chemin de sortie
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(os.path.dirname(base_dir), "data_lake", "bus")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "localisation_bus_paris.csv")

# Création des bus
bus_infos = []
bus_id = 1
for ligne in ares_par_ligne.keys():
    for i in range(10):  # 10 bus par ligne
        bus_infos.append({"id": bus_id, "ligne": ligne})
        bus_id += 1

# Génération du fichier
with open(output_file, mode="w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "ligne", "gare_depart", "destination", "position_gps", "heure_de_captage"])
    base_time = datetime(2025, 7, 1, 6, 0, 0)
    for bus in bus_infos:
        ligne = bus["ligne"]
        stops = ares_par_ligne[ligne]
        lat_base = 48.85
        lon_base = 2.35
        for ordre, arret in enumerate(stops[:-1]):
            gare_depart = arret
            destination = stops[ordre + 1]
            lat = lat_base + random.uniform(-0.01, 0.01)
            lon = lon_base + random.uniform(-0.01, 0.01)
            heure_captage = base_time + timedelta(minutes=5 * ordre + 3 * bus["id"] + 2)
            writer.writerow([
                bus["id"],
                ligne,
                gare_depart,
                destination,
                f"{lat:.5f},{lon:.5f}",
                heure_captage.strftime("%d/%m/%Y %H:%M")
            ])

print(f"Fichier généré dans : {output_file}")
