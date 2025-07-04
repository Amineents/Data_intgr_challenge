import subprocess
from pathlib import Path

# Dossier contenant les scripts
base_dir = Path(__file__).resolve().parent
ml_dir = base_dir / "ml"

# Scripts à exécuter
scripts = ["model_train_bus.py", "detect_lamp.py"]

for script in scripts:
    script_path = ml_dir / script
    print(f"\n--- Exécution de : {script} ---")
    
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=60  # Limite de temps par script (en secondes)
        )

        if result.returncode == 0:
            print("Script exécuté avec succès :")
            print(result.stdout)
        else:
            print(f"Erreur dans {script} (code {result.returncode}):")
            print(result.stderr)

    except subprocess.TimeoutExpired:
        print(f"Timeout : le script {script} a dépassé le délai autorisé.")
