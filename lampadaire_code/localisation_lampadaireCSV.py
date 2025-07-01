import requests
import os 

csv_url = "https://www.datasud.fr/fr/datapusher/ws/default/usergroup554.623aaaae-5d9c-4c14-aba3-9cab9c6bd58b/all.csv?maxfeatures=1000&start=1&filename=reseau-d-eclairage-public-ccpop-2-3"


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


folder_path = os.path.join(parent_dir, "data_lake", "lampadaires")
os.makedirs(folder_path, exist_ok=True)  


output_path = os.path.join(folder_path, "lampadaires_datasud.csv")

response = requests.get(csv_url)
if response.status_code == 200:
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("Fichier CSV sauvegardé avec succès :", output_path)
else:
    print("Erreur lors du téléchargement :", response.status_code)
