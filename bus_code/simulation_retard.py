import csv
import random
from datetime import datetime, timedelta

# Lignes et leurs gares (comme dans ton dictionnaire)
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

# On va créer 10 bus par ligne, donc id_bus de 1 à 150 (15 lignes x 10 bus)
bus_par_ligne = 10

def random_time(start_hour=8, end_hour=9):
    """Génère une heure aléatoire au format HH:MM entre start_hour et end_hour."""
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return datetime.strptime(f"{hour}:{minute}", "%H:%M")

# Génération des données de retard
historique_retards = []

id_bus_global = 1  # compteur d'id bus

for ligne, gares in ares_par_ligne.items():
    # Chaque ligne a 10 bus
    for bus_num in range(bus_par_ligne):
        id_bus = id_bus_global
        id_bus_global += 1

        gare_depart = gares[0]  # La première gare comme départ

        # On génère plusieurs retards aléatoires (entre 3 et 6 retards par bus)
        nb_retards = random.randint(3, 6)

        for _ in range(nb_retards):
            # Choisir une gare de retard (différente du départ)
            gare_retard = random.choice(gares[1:])
            
            heure_prevue = random_time()
            # Heure réelle = prévue + un retard aléatoire de 1 à 15 minutes
            retard = timedelta(minutes=random.randint(1, 15))
            heure_reelle = heure_prevue + retard
            
            historique_retards.append({
                "id_bus": id_bus,
                "ligne": ligne,
                "gare_depart": gare_depart,
                "gare_retard": gare_retard,
                "heure_arrivee_prevue": heure_prevue.strftime("%H:%M"),
                "heure_arrivee_reelle": heure_reelle.strftime("%H:%M")
            })

# Écriture dans un fichier CSV
with open("historique_retard.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id_bus", "ligne", "gare_depart", "gare_retard", "heure_arrivee_prevue", "heure_arrivee_reelle"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in historique_retards:
        writer.writerow(row)
