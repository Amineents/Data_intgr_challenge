import csv
import random
from datetime import datetime, timedelta

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

# Liste des lignes disponibles
lignes = list(ares_par_ligne.keys())

# Nombre total de bus à simuler
nb_bus = 150

def random_time(start_hour=6, end_hour=10):
    """Retourne une heure au format HH:MM aléatoire entre start_hour et end_hour."""
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def time_add_minutes(time_str, minutes):
    """Ajoute des minutes à une heure donnée au format HH:MM."""
    t = datetime.strptime(time_str, "%H:%M")
    t += timedelta(minutes=minutes)
    return t.strftime("%H:%M")

with open("historique_retard.csv", mode="w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id_bus", "ligne", "gare_depart", "gare_retard", "heure_arrivee_prevue", "heure_arrivee_reelle"])

    for bus_id in range(1, nb_bus + 1):
        # Attribuer une ligne au bus (rotation simple sur la liste)
        ligne = lignes[(bus_id - 1) % len(lignes)]
        gares = ares_par_ligne[ligne]
        
        gare_depart = gares[0]

        # Nombre de retards à générer par bus (entre 3 et 7)
        nb_retards = random.randint(3, 7)

        for _ in range(nb_retards):
            # Choisir une gare de retard différente de la gare_depart
            gare_retard = random.choice(gares[1:])  # au moins la deuxième gare

            # Générer une heure d'arrivée prévue entre 6h00 et 10h00
            heure_arrivee_prevue = random_time()

            # Retard entre 0 et 15 minutes
            retard = random.randint(0, 15)

            heure_arrivee_reelle = time_add_minutes(heure_arrivee_prevue, retard)

            writer.writerow([
                bus_id,
                ligne,
                gare_depart,
                gare_retard,
                heure_arrivee_prevue,
                heure_arrivee_reelle
            ])
