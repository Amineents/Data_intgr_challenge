import csv
from datetime import datetime, timedelta
import random
from pathlib import Path

#  Dossier cible correct
landing_dir = Path("../data_like/bus")
output_file = landing_dir / "horaires_arrets_bus.csv"

#  Liste des arrêts fixes par ligne
arrets_par_ligne = {
    "21": ["Stade Charléty", "Place d’Italie", "Glacière", "Denfert-Rochereau", "Raspail", "Gare Saint-Lazare"],
    "38": ["Gare du Nord", "Saint-Michel", "Cluny - La Sorbonne", "Luxembourg", "Alésia", "Porte d'Orléans"],
    "47": ["Fort du Kremlin", "Maison Blanche", "Place d’Italie", "Censier Daubenton", "Châtelet"],
    "63": ["Porte de la Muette", "Trocadéro", "Iéna", "Invalides", "Quai d’Orsay", "Gare de Lyon"],
    "72": ["Hôtel de Ville", "Pont Neuf", "Musée d'Orsay", "Trocadéro", "Boulogne Jean Jaurès", "Parc de Saint-Cloud"],
    "82": ["Luxembourg", "Port Royal", "Montparnasse", "Pasteur", "Convention", "Neuilly"],
    "91": ["Bastille", "Gare de Lyon", "Gobelins", "Glacière", "Raspail", "Montparnasse"],
    "96": ["Gare Montparnasse", "Rennes", "Saint-Germain-des-Prés", "Odéon", "République", "Porte des Lilas"],
    "27": ["Gare Saint-Lazare", "Opéra", "Pyramides", "Châtelet", "Quai de la Rapée", "Porte d’Ivry"],
    "69": ["Champ de Mars", "Invalides", "Assemblée Nationale", "Musée du Louvre", "Bastille", "Gambetta"],
    "24": ["Pont Neuf", "Hôtel de Ville", "Bastille", "Nation", "Montgallet", "École Militaire"],
    "52": ["La Muette", "Rue de la Pompe", "Trocadéro", "Iéna", "Madeleine", "Opéra"],
    "73": ["La Défense", "Neuilly", "Porte Maillot", "Charles de Gaulle - Étoile", "Champs-Élysées", "Musée d'Orsay"],
    "30": ["Porte Maillot", "Ternes", "Place Clichy", "Barbès", "Gare du Nord", "Gare de l'Est"],
    "87": ["Gare de Lyon", "Bercy", "Bibliothèque F. Mitterrand", "Olympiades", "Tolbiac", "Maison Blanche"]
}

#  Génération du fichier CSV
with output_file.open(mode="w", newline="", encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(["ligne", "nom_arret", "placement_gare", "heure_passage", "ordre_arret"])

    for ligne, arrets in arrets_par_ligne.items():
        heure_depart = datetime.now().replace(hour=random.randint(6, 10), minute=random.randint(0, 59), second=0, microsecond=0)

        for i, nom_arret in enumerate(arrets):
            placement = f"Arrêt {i+1} - Ligne {ligne}"
            heure_passage = heure_depart + timedelta(minutes=i * random.randint(3, 5))

            writer.writerow([
                ligne,
                nom_arret,
                placement,
                heure_passage.strftime("%Y-%m-%d %H:%M:%S"),
                i + 1
            ])

print(f"Fichier généré : {output_file}")
