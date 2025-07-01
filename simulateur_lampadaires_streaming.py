import json
import random
import time
from datetime import datetime
from pathlib import Path

# Préparation du dossier cible
landing_dir = Path("data_lake/landing/lampadaires")
landing_dir.mkdir(parents=True, exist_ok=True)

# Paramètres
output_file = landing_dir / "lampadaires_streaming_simulation.jsonl"
lamp_ids = [f"LAMP{str(i+1).zfill(3)}" for i in range(10)]
num_lines = 100  # Nombre de lignes à générer
interval_seconds = 1  # Intervalle entre chaque ligne (en secondes)

# Simulation de données en streaming
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
        f.flush()
        print(f"Écrit: {record}")
        time.sleep(interval_seconds)
