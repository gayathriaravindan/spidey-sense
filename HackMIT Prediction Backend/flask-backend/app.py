from flask import Flask, request
from flask_cors import CORS
import joblib
import requests

app = Flask(__name__)
CORS(app)
model = joblib.load("flask-backend/WESAD_binary_xgboost.pkl")

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Confirm data exists
    if not "heart_rate" in data:
        return {"error": "Missing heart_rate parameter"}, 400
    if not "x_acceleration" in data:
        return {"error": "Missing x_acceleration parameter"}, 400
    if not "y_acceleration" in data:
        return {"error": "Missing y_acceleration parameter"}, 400
    if not "z_acceleration" in data:
        return {"error": "Missing z_acceleration parameter"}, 400
    if "temperature" not in data:
        temperature = 5

    # Confirm data is strings
    if not isinstance(data["heart_rate"], (str, float, int)):
        return {"error": "Invalid heart_rate parameter: data type"}, 400
    if not isinstance(data["x_acceleration"], (str, float, int)):
        return {"error": "Invalid heart_rate parameter: data type"}, 400
    if not isinstance(data["y_acceleration"], (str, float, int)):
        return {"error": "Invalid heart_rate parameter: data type"}, 400
    if not isinstance(data["z_acceleration"], (str, float, int)):
        return {"error": "Invalid heart_rate parameter: data type"}, 400
    
    # Confirm data can be cast
    if not is_float(data["heart_rate"]):
        return {"error": "Invalid heart_rate parameter"}, 400
    if not is_float(data["x_acceleration"]):
        return {"error": "Invalid x_acceleration parameter"}, 400
    if not is_float(data["y_acceleration"]):
        return {"error": "Invalid y_acceleration parameter"}, 400
    if not is_float(data["z_acceleration"]):
        return {"error": "Invalid z_acceleration parameter"}, 400
    if not isinstance(data, str) or not data["temperature"].isnumeric():
        temperature = 5

    # Convert temperature to cutoff 
    if (int(temperature) < 1 or int(temperature) > 10):
        temperature = 5
    proba_cutoff = 0.5 + (0.05 * (5 - int(temperature)))

    heart_rate = float(data["heart_rate"])
    x_acceleration = float(data["x_acceleration"])
    y_acceleration = float(data["y_acceleration"])
    z_acceleration = float(data["z_acceleration"])

    # Convert acceleration to max range of E4 if necessary
    if x_acceleration > 2:
        x_acceleration = 2
    if x_acceleration < -2:
        x_acceleration = -2
    if y_acceleration > 2:
        y_acceleration = 2
    if y_acceleration < -2:
        y_acceleration = -2
    if z_acceleration > 2:
        z_acceleration = 2
    if z_acceleration < -2:
        z_acceleration = -2
    
    # Convert Bangle.js 2 unit to E4 unit
    x_acceleration *= 64
    y_acceleration *= 64
    z_acceleration *= 64

    prediction = model.predict_proba([[heart_rate, x_acceleration, y_acceleration, z_acceleration]])[0][1]

    predBool = "normal" if prediction.item() < proba_cutoff else "anomaly"

    if predBool == "anomaly":
        url = "https://4d44-192-54-222-158.ngrok-free.app/start_call"
        response = requests.get(url)
        if (not response.status_code == 200):
            print('err')

    return {"prediction": predBool}
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)