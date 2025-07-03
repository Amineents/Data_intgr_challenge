import os
import subprocess
from pathlib import Path

# Répertoires contenant les scripts de transformation
BASE_DIR = Path(__file__).resolve().parent
TRANSFORMATION_DIR = BASE_DIR / "transformation_code"

# Fichiers spécifiques à exécuter
scripts_a_executer = [
    TRANSFORMATION_DIR / "transformation_bus.py",
    TRANSFORMATION_DIR / "transformation_lampadaires.py"
]

# Exécution de chaque script
for script in scripts_a_executer:
    if script.exists():
        print(f" Exécution de : {script.name}")
        subprocess.run(["python", str(script)], check=True)
    else:
        print(f" Script introuvable : {script.name}")

print("Transformation terminée et chargée dans MySQL.")
