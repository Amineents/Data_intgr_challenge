# Data_intgr_challenge

# Projet Smart City – Pipeline de Données

Ce projet met en place un pipeline de traitement de données pour une ville intelligente, combinant ingestion, transformation, enrichissement, machine learning, et visualisation dans Power BI.

---

##  Structure du projet

```
.
├── data_lake/                      # Données sources simulées (bus, lampadaires, météo...)
├── transformation_code/           # Scripts de transformation vers la couche Silver
├── ml/                            # Scripts de machine learning (entraînement modèles)
├── create_gold.py                 # Création des tables Gold dans MySQL
├── ml_excute.py                   # Exécution des modèles ML
├── transformations_silver.py     # Pipeline de transformation Silver
├── ingestion.py                   # Simulation de l’ingestion des fichiers
├── pipeline.py                    # Pipeline d’orchestration global
└── README.md                      # Ce fichier
```

---

##  Exécution du pipeline

Tu peux exécuter tout le pipeline avec un seul script :

```bash
python pipeline.py
```

Ce script :

1. Lance `ingestion.py`
2. Lance `transformations_silver.py`
3. En parallèle :
   - `create_gold.py` (remplit les tables Gold dans MySQL)
   - `ml_excute.py` (entraîne les modèles de ML)

---

## Visualisation

Power BI est connecté à la base `golden_bus_lamp` via ODBC.

### Graphiques :

- **Bus**
  - Nombre de retards par ligne
  - Retard moyen par météo
  - Retard moyen par gare de départ

- **Lampadaires**
  - Consommation moyenne par lampadaire
  - Répartition des marques de lampadaires
  - Nombre de lampes utilisées par jour (et par mois)

---

## Technologies utilisées

- Python 3.11+
- Pandas
- MySQL
- Power BI
- Git

---

## Branches Git
Le projet est versionné avec Git et contient les branches suivantes :

- `main` : branche principale contenant la version stable du projet.
- `dev_amine` : branche de développement d'Amine.
- `dev_aymen` : branche de développement d’Aymene.
- `dev_nina` : branche de développement de Thanina.

---

## Auteurs

- **Amine Naitsidhoum**
- **Thanina Guernine**
- **Aymene Meziane**

---


## Licence
Ce projet est un travail académique réalisé sous l'encadrement de l'école **EFREI Paris**.

