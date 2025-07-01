import csv
import random
from datetime import datetime, timedelta

# Lignes avec leurs arrêts fixes
arrets_par_ligne = {
    "21": ["Gare Saint-Lazare", "Opéra", "Louvre", "Châtelet", "Bastille", "Gare de Lyon"],
    "38": ["Gare du Nord", "République", "Hôtel de Ville", "Saint-Michel", "Denfert-Rochereau", "Porte d'Orléans"],
    "72": ["Parc André Citroën", "Tour Eiffel", "Invalides", "Musée d'Orsay", "Louvre", "Hôtel de Ville"],
    "91": ["Gare Montparnasse", "Raspail", "Denfert-Rochereau", "Glacière", "Place d'Italie", "Bibliothèque F. Mitterrand"],
    "31": ["Porte de Champerret", "Wagram", "Place de Clichy", "Trinité", "Chaussée d’Antin", "Opéra"],
    "24": ["Gare Saint-Lazare", "Saint-Augustin", "Opéra", "Louvre", "Pont Neuf", "Saint-Michel"],
    "26": ["Nation", "Avron", "Buzenval", "Maraîchers", "Porte de Bagnolet", "Gallieni"],
    "56": ["Porte de Clignancourt", "Simplon", "Marcadet", "Jules Joffrin", "Guy Môquet", "Place de Clichy"],
    "52": ["Gare Saint-Lazare", "Europe", "Rome", "Villiers", "Porte de Clichy", "Mairie de Clichy"],
    "39": ["Issy", "Corentin Celton", "Convention", "Volontaires", "Sèvres-Lecourbe", "Montparnasse"],
    "62": ["Porte de Saint-Cloud", "Exelmans", "Michel-Ange", "Porte de Versailles", "Porte de Vanves", "Alésia"],
    "73": ["La Défense", "Pont de Neuilly", "Argentine", "Charles de Gaulle-Étoile", "George V", "Champs-Élysées"],
    "68": ["Châtillon", "Malakoff", "Porte de Vanves", "Alésia", "Denfert-Rochereau", "Montparnasse"],
    "80": ["Mairie du 18e", "Place Clichy", "Saint-Lazare", "Opéra", "Madeleine", "Invalides"],
    "92": ["Porte de Champerret", "Péreire", "Courcelles", "Monceau", "Miromesnil", "Madeleine"]
}

with open("historique_retards.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id_bus", "ligne", "gare_depart", "gare_retard", "heure_arrivee_prevue", "heure_arrivee_reelle"])
    
    bus_counter = 1

    for ligne, arrets in arrets_par_ligne.items():
        nb_retards = random.randint(1, 5)  # nombre de retards par ligne

        for _ in range(nb_retards):
            id_bus = bus_counter
            gare_depart = arrets[0]  # premier arrêt (nom)
            num_gare_retard = random.randint(1, len(arrets)-1)  # indice aléatoire sauf premier arrêt
            gare_retard = arrets[num_gare_retard]

            heure_base = datetime.strptime("08:00", "%H:%M")
            minute_offset = (num_gare_retard + 1) * 5
            heure_prevue = heure_base + timedelta(minutes=minute_offset)

            retard = random.randint(1, 10)
            heure_reelle = heure_prevue + timedelta(minutes=retard)

            writer.writerow([
                id_bus,
                ligne,
                gare_depart,
                gare_retard,
                heure_prevue.strftime("%H:%M"),
                heure_reelle.strftime("%H:%M")
            ])

            bus_counter += 1
