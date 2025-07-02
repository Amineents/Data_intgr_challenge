import json
import random
from datetime import datetime, timedelta
from pathlib import Path

current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent 

lamp_dir = base_dir / "data_lake" / "lampadaires"
lamp_dir.mkdir(parents=True, exist_ok=True)

# Fichier de sortie
output_file = lamp_dir / "reclamations_lampadaires.jsonl"


# Paramètres de simulation
lamp_ids = [f"LAMP{str(i+1).zfill(3)}" for i in range(500)]
statuses = ["off", "blinking", "broken", "on_but_dim"]
num_reports = 600
start_time = datetime.now() - timedelta(days=5)

# Génération des réclamations
with output_file.open("w", encoding="utf-8") as f:
    for _ in range(num_reports):
        record = {
            "lamp_id": random.choice(lamp_ids),
            "report_time": (start_time + timedelta(minutes=random.randint(0, 7200))).isoformat(),
            "status": random.choice(statuses)
        }
        f.write(json.dumps(record) + "\n")
        print(f"Généré : {record}")

print(f"\n Fichier généré : {output_file}")
