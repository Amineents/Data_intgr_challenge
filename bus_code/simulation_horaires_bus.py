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

bus_infos = []
bus_id = 1
for ligne in ares_par_ligne.keys():
    for i in range(10):  # 10 bus par ligne
        bus_infos.append({"id": bus_id, "ligne": ligne})
        bus_id += 1

# Déterminer dynamiquement le chemin de sortie
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(current_dir), "data_lake", "bus")
os.makedirs(data_dir, exist_ok=True)
output_file = os.path.join(data_dir, "horaires_bus.csv")

# Génération du fichier
with open(output_file, mode="w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ligne", "nom_arret", "placement_gare", "heure_passage", "ordre_arret"])

    base_time = datetime(2025, 7, 1, 6, 0, 0)

    for bus in bus_infos:
        ligne = bus["ligne"]
        stops = ares_par_ligne[ligne]
        for ordre, arret in enumerate(stops):
            heure_passage = base_time + timedelta(minutes=5 * ordre + 3 * bus["id"])
            placement_gare = f"Arrêt {ordre} - Ligne {ligne}"
            writer.writerow([ligne, arret, placement_gare, heure_passage.strftime("%Y-%m-%d %H:%M:%S"), ordre])

print(f"Fichier généré dans : {output_file}")
