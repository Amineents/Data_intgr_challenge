import requests


csv_url = "https://www.datasud.fr/fr/datapusher/ws/default/usergroup554.623aaaae-5d9c-4c14-aba3-9cab9c6bd58b/all.csv?maxfeatures=1000&start=1&filename=reseau-d-eclairage-public-ccpop-2-3"


output_path = "../data_like/lampadaires/lampadaires_datasud.csv"


response = requests.get(csv_url)
if response.status_code == 200:
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("Fichier CSV sauvegardé avec succès :", output_path)
else:
    print("Erreur lors du téléchargement :", response.status_code)
