import joblib
import sklearn

model = joblib.load("WESAD_binary_xgboost.pkl")
probs = model.predict_proba([[0, 0, 0, 0]])