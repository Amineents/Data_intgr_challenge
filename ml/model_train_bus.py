import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import joblib

# 1. Connexion à MySQL et chargement des données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    database="bus_silver"
)

# Chargement des données
df_retards = pd.read_sql("SELECT * FROM historique_retards", conn)
df_weather = pd.read_sql("SELECT * FROM weather", conn)
df_trafic = pd.read_sql("SELECT * FROM trafic_routes", conn)

# 2. Préparation des données
df_retards["heure_arrivee_prevue"] = pd.to_datetime(df_retards["heure_arrivee_prevue"], errors='coerce')
df_retards["heure_arrivee_reelle"] = pd.to_datetime(df_retards["heure_arrivee_reelle"], errors='coerce')
df_weather["timestamp"] = pd.to_datetime(df_weather["timestamp"], errors='coerce')
df_trafic["timestamp"] = pd.to_datetime(df_trafic["timestamp"], errors='coerce')

df_retards["retard_minutes"] = (
    df_retards["heure_arrivee_reelle"] - df_retards["heure_arrivee_prevue"]
).dt.total_seconds() / 60

df_retards = df_retards.dropna(subset=["retard_minutes", "heure_arrivee_prevue"])

df_joined = pd.merge_asof(
    df_retards.sort_values("heure_arrivee_prevue"),
    df_weather.sort_values("timestamp"),
    left_on="heure_arrivee_prevue",
    right_on="timestamp",
    direction="backward"
)

df_joined = pd.merge_asof(
    df_joined.sort_values("heure_arrivee_prevue"),
    df_trafic[df_trafic["route_to"].notna()].sort_values("timestamp"),
    left_on="heure_arrivee_prevue",
    right_on="timestamp",
    left_by="gare_retard",
    right_by="route_to",
    direction="backward"
)

# 3. Sélection et imputation des colonnes
df_model = df_joined[[
    "ligne", "gare_depart", "gare_retard",
    "temperature", "humidity", "wind_speed", "cloud_percent",
    "traffic_level", "vehicle_count", "avg_speed_kmh",
    "retard_minutes"
]].copy()

# ➤ Imputation (remplir les NaN avec des valeurs par défaut/moyennes)
print("Nombre de NaN avant imputation :\n", df_model.isna().sum())

num_cols = ["temperature", "humidity", "wind_speed", "cloud_percent", "vehicle_count", "avg_speed_kmh"]
cat_cols = ["ligne", "gare_depart", "gare_retard", "traffic_level"]

for col in num_cols:
    df_model[col].fillna(df_model[col].mean(), inplace=True)

for col in cat_cols:
    df_model[col].fillna("inconnu", inplace=True)

# Filtrage final des lignes où la target serait encore NaN (par précaution)
df_model.dropna(subset=["retard_minutes"], inplace=True)

print("Nombre de NaN après imputation :\n", df_model.isna().sum())

# 4. Encodage des variables catégorielles
X_cat = df_model[cat_cols]
X_num = df_model.drop(columns=cat_cols + ["retard_minutes"])

encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_cat_encoded = encoder.fit_transform(X_cat)
X_cat_encoded = pd.DataFrame(X_cat_encoded, columns=encoder.get_feature_names_out(cat_cols))

X = pd.concat([X_num.reset_index(drop=True), X_cat_encoded], axis=1)
y = df_model["retard_minutes"].reset_index(drop=True)

# 5. Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Modélisation
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Évaluation
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nMAE (Erreur absolue moyenne) : {mae:.2f} minutes")
print(f"R² (Score de performance) : {r2:.2f}")

# 8. Visualisation
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Retards réels (minutes)")
plt.ylabel("Retards prédits (minutes)")
plt.title("Prédiction des retards de bus")
plt.grid(True)
plt.show()

# 9. Sauvegarde
joblib.dump(model, "modele_retard_bus.pkl")
joblib.dump(encoder, "encoder_bus.pkl")

conn.close()
