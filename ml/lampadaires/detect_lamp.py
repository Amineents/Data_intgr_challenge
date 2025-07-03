import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Connection details based on your Docker command
MYSQL_USER = 'root'                    
MYSQL_PASSWORD = 'my-secret-pw'                
MYSQL_HOST = 'localhost'               
MYSQL_PORT = 3306                      
MYSQL_DB = 'lampadaires_silver'              

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# Step 1: Load labeled data (example: lamp-day with is_faulty label)
labeled_query = """
WITH recent_complaints AS (
  SELECT lamp_id, DATE(report_time) AS report_date, status
  FROM reclamations_lampadaires
  WHERE status IN ('broken', 'on_but_dim', 'off')
),
faulty_lamps AS (
  SELECT DISTINCT lamp_id, report_date FROM recent_complaints
),
date_range AS (
  SELECT DISTINCT DATE(ts) AS day_date FROM consommation_lampadaires
),
lamp_dates AS (
  SELECT DISTINCT lamp_id, day_date
  FROM consommation_lampadaires
  CROSS JOIN date_range
),
labeled_data AS (
  SELECT
    ld.lamp_id,
    ld.day_date,
    CASE WHEN EXISTS (
      SELECT 1 FROM faulty_lamps fl
      WHERE fl.lamp_id = ld.lamp_id
      AND fl.report_date BETWEEN DATE_SUB(ld.day_date, INTERVAL 7 DAY) AND ld.day_date
    ) THEN 1 ELSE 0 END AS is_faulty
  FROM lamp_dates ld
)
SELECT * FROM labeled_data
"""

labeled_df = pd.read_sql(labeled_query, engine)

# Step 2: Aggregate consumption stats per lamp per day
consumption_query = """
SELECT
  lamp_id,
  DATE(ts) AS day_date,
  AVG(consumption_kwh) AS avg_consumption,
  STDDEV(consumption_kwh) AS std_consumption,
  MAX(consumption_kwh) AS max_consumption,
  MIN(consumption_kwh) AS min_consumption
FROM consommation_lampadaires
GROUP BY lamp_id, day_date
"""
consumption_df = pd.read_sql(consumption_query, engine)

# Step 3: Load lamp static info
static_df = pd.read_sql("SELECT * FROM lampadaires_static", engine)

# Step 4: Load planning_allumage - average on_time and off_time per lamp per day
planning_query = """
SELECT
  lamp_id,
  date AS day_date,
  TIME_TO_SEC(on_time) AS on_seconds,
  TIME_TO_SEC(off_time) AS off_seconds
FROM planning_allumage
"""
planning_df = pd.read_sql(planning_query, engine)

# Aggregate average on/off seconds per lamp/day (in case of multiple rows)
planning_agg = planning_df.groupby(['lamp_id', 'day_date']).agg({
    'on_seconds': 'mean',
    'off_seconds': 'mean'
}).reset_index()

# Step 5: Load sunrise_sunset (use day_date and get day length in seconds)
sun_query = """
SELECT DATE(timestamp) AS day_date, AVG(day_length) AS avg_day_length
FROM sunrise_sunset
GROUP BY day_date
"""
sun_df = pd.read_sql(sun_query, engine)

# Step 6: Merge all dataframes on lamp_id and day_date
df = labeled_df.merge(consumption_df, on=['lamp_id', 'day_date'], how='left')
df = df.merge(planning_agg, on=['lamp_id', 'day_date'], how='left')
df = df.merge(sun_df, on='day_date', how='left')
df = df.merge(static_df, on='lamp_id', how='left')

# Step 7: Feature engineering & cleaning

# Convert categorical static columns to numeric labels
categorical_cols = ['marque', 'etat_foy', 'type_amp', 'etat_cro', 'vasque']
for col in categorical_cols:
    df[col] = df[col].fillna('unknown')
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Fill missing numerical values with median or 0
num_cols = ['avg_consumption', 'std_consumption', 'max_consumption', 'min_consumption', 
            'on_seconds', 'off_seconds', 'avg_day_length']
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Extract time features from day_date
df['day_date'] = pd.to_datetime(df['day_date'])
df['day_of_week'] = df['day_date'].dt.dayofweek

# Optional: add interaction features (e.g., consumption relative to day length)
df['consumption_per_day_length'] = df['avg_consumption'] / (df['avg_day_length'] + 1)

# Step 8: Define features and target
features = ['avg_consumption', 'std_consumption', 'max_consumption', 'min_consumption', 
            'on_seconds', 'off_seconds', 'avg_day_length', 'day_of_week',
            'marque', 'etat_foy', 'type_amp', 'etat_cro', 'vasque',
            'consumption_per_day_length']

X = df[features]
y = df['is_faulty']

# Step 9: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Step 10: Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
clf.fit(X_train, y_train)

# Step 11: Evaluate
y_pred = clf.predict(X_test)

print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
