import subprocess
from pathlib import Path
import threading

# Répertoire de base
base_dir = Path(__file__).resolve().parent

# Scripts
script_ingest = base_dir / "ingestion.py"
script_silver = base_dir / "transformations_silver.py"
script_gold = base_dir / "create_gold.py"
script_ml = base_dir / "ml_excute.py"

def run_script(script_path):
    print(f"Exécution de : {script_path.name}")
    result = subprocess.run(["python", str(script_path)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Erreur dans {script_path.name} :\n{result.stderr}")
    else:
        print(f"termine : {script_path.name}\n")

# Étapes séquentielles : ingestion et transformation_silver
run_script(script_ingest)
run_script(script_silver)

# Étapes parallèles : create_gold et ml_excute
t1 = threading.Thread(target=run_script, args=(script_gold,))
t2 = threading.Thread(target=run_script, args=(script_ml,))
t1.start()
t2.start()

# Attendre la fin des 2
t1.join()
t2.join()

print("Pipeline complet (silver → gold & ML exécutés en parallèle).")
