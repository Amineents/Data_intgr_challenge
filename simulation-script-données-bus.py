import csv
import random
from datetime import datetime, timedelta

# 15 lignes de bus fictives
lignes_bus = [
    {"ligne": "21", "gare_depart": "Stade Charléty", "destination": "Gare Saint-Lazare"},
    {"ligne": "38", "gare_depart": "Gare du Nord", "destination": "Porte d'Orléans"},
    {"ligne": "47", "gare_depart": "Fort du Kremlin", "destination": "Châtelet"},
    {"ligne": "63", "gare_depart": "Porte de la Muette", "destination": "Gare de Lyon"},
    {"ligne": "72", "gare_depart": "Hôtel de Ville", "destination": "Parc de Saint-Cloud"},
    {"ligne": "82", "gare_depart": "Luxembourg", "destination": "Neuilly"},
    {"ligne": "91", "gare_depart": "Bastille", "destination": "Montparnasse"},
    {"ligne": "96", "gare_depart": "Gare Montparnasse", "destination": "Porte des Lilas"},
    {"ligne": "27", "gare_depart": "Gare Saint-Lazare", "destination": "Porte d’Ivry"},
    {"ligne": "69", "gare_depart": "Champ de Mars", "destination": "Gambetta"},
    {"ligne": "24", "gare_depart": "Pont Neuf", "destination": "École Militaire"},
    {"ligne": "52", "gare_depart": "La Muette", "destination": "Opéra"},
    {"ligne": "73", "gare_depart": "La Défense", "destination": "Musée d'Orsay"},
    {"ligne": "30", "gare_depart": "Porte Maillot", "destination": "Gare de l'Est"},
    {"ligne": "87", "gare_depart": "Gare de Lyon", "destination": "Bibliothèque F. Mitterrand"},
]

with open("donnees_bus_paris.csv", mode="w", newline="", encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow([
        "id", "ligne", "gare_depart", "destination", "position_gps",
        "heure_de_captage", "depart"
    ])

    for idx, ligne in enumerate(lignes_bus, start=1):
        lat = round(random.uniform(48.80, 48.90), 6)
        lon = round(random.uniform(2.30, 2.42), 6)
        position = f"{lat},{lon}"

        heure_captage = datetime.now()
        delta_depart = timedelta(minutes=random.randint(5, 15))
        heure_depart = heure_captage - delta_depart

        writer.writerow([
            idx,
            ligne["ligne"],
            ligne["gare_depart"],
            ligne["destination"],
            position,
            heure_captage.strftime("%Y-%m-%d %H:%M:%S"),
            heure_depart.strftime("%Y-%m-%d %H:%M:%S")
        ])

print("✅ Fichier 'donnees_bus_paris.csv' généré sans colonne trafic.")
def afficher_lignes_bus(lignes_bus):
    print("📋 Liste des lignes de bus :\n")
    for ligne in lignes_bus:
        print(f"Ligne {ligne['ligne']} : de {ligne['gare_depart']} → {ligne['destination']}")
afficher_lignes_bus(lignes_bus)