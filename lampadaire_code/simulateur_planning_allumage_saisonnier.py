import pandas as pd
from datetime import datetime
from pathlib import Path

#  Dossier de sortie
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent 

lamp_dir = base_dir / "data_lake" / "lampadaires"
lamp_dir.mkdir(parents=True, exist_ok=True)

# Fichier de sortie
output_file = lamp_dir / "planning_allumage_saisonnier.csv"



#  Paramètres
lamp_ids = [f"LAMP{str(i+1).zfill(3)}" for i in range(100)]
dates = pd.date_range(start="2025-05-28", periods=10, freq="D")

def is_summer(date):
    # Été défini de mai à août
    return date.month in [5, 6, 7, 8]

# Génération du planning
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

# Sauvegarde CSV
df = pd.DataFrame(planning)
df.to_csv(output_file, index=False, encoding="utf-8")
print(f" Fichier généré : {output_file}")
