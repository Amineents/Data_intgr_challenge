import csv
import random
from datetime import datetime, timedelta

# Dictionnaire : ligne → liste de gares (arrêts)
gares_par_ligne = {
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

# Bus liés à une seule ligne
bus_infos = [
    {"id": 1, "ligne": "21"},
    {"id": 2, "ligne": "38"},
    {"id": 3, "ligne": "47"},
    {"id": 4, "ligne": "63"},
    {"id": 5, "ligne": "72"},
    {"id": 6, "ligne": "82"},
    {"id": 7, "ligne": "91"},
    {"id": 8, "ligne": "96"},
    {"id": 9, "ligne": "27"},
    {"id": 10, "ligne": "69"},
    {"id": 11, "ligne": "24"},
    {"id": 12, "ligne": "52"},
    {"id": 13, "ligne": "73"},
    {"id": 14, "ligne": "30"},
    {"id": 15, "ligne": "87"}
]

# Création du fichier CSV des retards
with open("historique_retards.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id_bus", "ligne", "gare_depart", "gare_retard", "heure_arrivee_prevue", "heure_arrivee_reelle"])

    for bus in bus_infos:
        ligne = bus["ligne"]
        arrets = gares_par_ligne[ligne]
        gare_depart = arrets[0]

        nb_retards = random.randint(2, 4)

        for _ in range(nb_retards):
            gare_retard = random.choice(arrets[1:])  # on ne prend pas la gare de départ

            heure_base = datetime.strptime("08:00", "%H:%M")
            offset_min = random.randint(10, 50)
            heure_prevue = heure_base + timedelta(minutes=offset_min)

            retard_min = random.randint(2, 15)
            heure_reelle = heure_prevue + timedelta(minutes=retard_min)

            writer.writerow([
                bus["id"],
                ligne,
                gare_depart,
                gare_retard,
                heure_prevue.strftime("%H:%M"),
                heure_reelle.strftime("%H:%M")
            ])
