from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np

app = Flask(__name__)

# Load the data from the CSV file
data = pd.read_csv('_crop+yield+prediction_data_crop_yield.csv')

# Preprocess the data
X = data.drop(['Crop', 'Yield'], axis=1)
y = data['Yield']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train the Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

def predict_yield(crop, precipitation, specific_humidity, relative_humidity, temperature):
    try:
        # Create a new data point
        new_data = np.array([[precipitation, specific_humidity, relative_humidity, temperature]])
        # Preprocess the new data point
        new_data_scaled = scaler.transform(new_data)
        # Predict the yield
        predicted_yield = model.predict(new_data_scaled)
        return predicted_yield[0]
    except Exception as e:
        return f"Error in prediction: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        crop = request.form['crop']
        precipitation = float(request.form['precipitation'])
        specific_humidity = float(request.form['specific_humidity'])
        relative_humidity = float(request.form['relative_humidity'])
        temperature = float(request.form['temperature'])

        # Validate inputs
        if not (0 <= precipitation <= 1000 and 0 <= specific_humidity <= 100 and 0 <= relative_humidity <= 100 and -50 <= temperature <= 50):
            return jsonify({"error": "Invalid input values!"})

        predicted_yield = predict_yield(crop, precipitation, specific_humidity, relative_humidity, temperature)
        
        return jsonify({
            "crop": crop,
            "predicted_yield": predicted_yield,
            "inputs": {
                "precipitation": precipitation,
                "specific_humidity": specific_humidity,
                "relative_humidity": relative_humidity,
                "temperature": temperature
            }
        })
    except Exception as e:
        return jsonify({"error": f"Error in processing: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
