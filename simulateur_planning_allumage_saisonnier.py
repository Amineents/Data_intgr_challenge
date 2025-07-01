import pandas as pd
from datetime import datetime
from pathlib import Path

# Préparation du dossier cible
landing_dir = Path("data_lake/landing/lampadaires")
landing_dir.mkdir(parents=True, exist_ok=True)

# Paramètres
lamp_ids = [f"LAMP{str(i+1).zfill(3)}" for i in range(10)]
dates = pd.date_range(start="2025-06-28", periods=10, freq="D")

def is_summer(date):
    # On considère que l'été est de mai à août
    return date.month in [5, 6, 7, 8]

planning = []

for lamp_id in lamp_ids:
    for date in dates:
        if is_summer(date):
            on_time = "22:00"
            off_time = "05:00"
        else:
            on_time = "18:00"
            off_time = "06:00"

        planning.append({
            "lamp_id": lamp_id,
            "date": date.date().isoformat(),
            "on_time": on_time,
            "off_time": off_time
        })

# Export CSV dans dossier landing/lampadaires
output_file = landing_dir / "planning_allumage_saisonnier.csv"
df = pd.DataFrame(planning)
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Fichier '{output_file}' généré.")
