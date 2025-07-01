import json
import random
import time
from datetime import datetime
from pathlib import Path


#  Dossier de sortie
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent 

landing_dir = base_dir / "data_lake" / "lampadaires"
landing_dir.mkdir(parents=True, exist_ok=True)

# Fichier de sortie
output_file = landing_dir / "lampadaires_streaming_simulation.jsonl"



#  Paramètres de simulation
lamp_ids = [f"LAMP{str(i+1).zfill(3)}" for i in range(10)]
num_lines = 100  # Nombre de lignes à générer


#  Simulation de données de consommation électrique en streaming
with output_file.open("w", encoding="utf-8") as f:
    for _ in range(num_lines):
        lamp_id = random.choice(lamp_ids)
        ts = datetime.now().isoformat()
        consumption_kwh = round(random.uniform(0.1, 0.8), 2)

        record = {
            "lamp_id": lamp_id,
            "ts": ts,
            "consumption_kwh": consumption_kwh
        }

        f.write(json.dumps(record) + "\n")
        f.flush()  # Pour simuler un flux en temps réel
        print(f"Écrit: {record}")

print(f"\n Fichier généré : {output_file}")
