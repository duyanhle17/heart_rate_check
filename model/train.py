import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/hr_history.csv")
X = df[["hr"]].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_scaled)

joblib.dump(model, "model/hr_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model trained")
