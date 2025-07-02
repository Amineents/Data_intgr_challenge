
import os
import subprocess
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent
DATA_LAKE_DIR = BASE_DIR / "data_lake"
BUS_CODE_DIR = BASE_DIR / "bus_code"
LAMPADAIRE_CODE_DIR = BASE_DIR / "lampadaire_code"

# 1. Vérifier et créer data_lake/
if not DATA_LAKE_DIR.exists():
    print(" Création du dossier data_lake...")
    DATA_LAKE_DIR.mkdir(parents=True)
else:
    print("Le dossier data_lake existe déjà.")

# 2. Fonction pour exécuter tous les fichiers .py dans un dossier
def executer_scripts_python(dossier: Path):
    print(f"\nExécution des scripts dans : {dossier.name}")
    for fichier in sorted(dossier.glob("*.py")):
        print(f"  Exécution de : {fichier.name}")
        subprocess.run(["python", str(fichier)], check=True)

# 3. Exécution des scripts
executer_scripts_python(BUS_CODE_DIR)
executer_scripts_python(LAMPADAIRE_CODE_DIR)

print("ingestion terminee")