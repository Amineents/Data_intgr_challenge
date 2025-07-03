import csv
import random
import os
from datetime import datetime, timedelta

# === Définition des arrêts par ligne ===
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

bus_par_ligne = 10

def random_time(start_hour=8, end_hour=9):
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return datetime.strptime(f"{hour}:{minute}", "%H:%M")

# === Génération des retards ===
historique_retards = []
id_bus_global = 1

for ligne, gares in ares_par_ligne.items():
    for _ in range(bus_par_ligne):
        id_bus = id_bus_global
        id_bus_global += 1

        gare_depart = gares[0]
        nb_retards = random.randint(3, 6)

        for _ in range(nb_retards):
            gare_retard = random.choice(gares[1:])
            heure_prevue = random_time()
            heure_reelle = heure_prevue + timedelta(minutes=random.randint(1, 15))

            historique_retards.append({
                "id_bus": id_bus,
                "ligne": ligne,
                "gare_depart": gare_depart,
                "gare_retard": gare_retard,
                "heure_arrivee_prevue": heure_prevue.strftime("%H:%M"),
                "heure_arrivee_reelle": heure_reelle.strftime("%H:%M")
            })

# === Écriture dans data_lake/bus/historique_retards.csv ===
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(current_dir), "data_lake", "bus")
os.makedirs(data_dir, exist_ok=True)
output_file = os.path.join(data_dir, "historique_retards.csv")

with open(output_file, mode="w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["id_bus", "ligne", "gare_depart", "gare_retard", "heure_arrivee_prevue", "heure_arrivee_reelle"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(historique_retards)

print(f"Fichier généré : {output_file}")
