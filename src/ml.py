import joblib

model = joblib.load("model/hr_model.pkl")
scaler = joblib.load("model/scaler.pkl")

def ml_check_hr(hr):
    x = scaler.transform([[hr]])
    pred = model.predict(x)[0]
    return "ABNORMAL" if pred == -1 else "NORMAL"
