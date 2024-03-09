from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import db, credentials
import math
import pickle
import json

app = Flask(__name__)

# Authenticate to Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://bees-9478f-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Creating reference to readings node
ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

def feeding_need():
    # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    rain_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest 5 records
    latest_rainfall = rain_ref.order_by_key().limit_to_last(10).get()

    if not latest_rainfall:
        return None  # Handle the case when there is no data

    # Extract freq values from the dictionary
    rain_values = []

    for value in latest_rainfall.values():
        try:
            rain = float(value.get("rainfall"))
            if not math.isnan(rain):  # Check for NaN
                rain_values.append(rain)
        except (ValueError, TypeError):
            # Handle the case when the value is not a valid float
            pass

    if rain_values:
        average_rain = sum(rain_values) / len(rain_values)
        return average_rain
    else:
        return None

def detect_swarming():
    # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    freq_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest 5 records
    latest_frequency = freq_ref.order_by_key().limit_to_last(10).get()

    if not latest_frequency:
        return None  # Handle the case when there is no data

    # Extract freq values from the dictionary
    freq_values = []

    for value in latest_frequency.values():
        try:
            freq = float(value.get("frequency"))
            if not math.isnan(freq):  # Check for NaN
                freq_values.append(freq)
        except (ValueError, TypeError):
            # Handle the case when the value is not a valid float
            pass

    if freq_values:
        average_freq = sum(freq_values) / len(freq_values)
        return average_freq
    else:
        return None

def get_live_data():
    # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    live_data_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest data
    latest_data = live_data_ref.order_by_key().limit_to_last(1).get()

    if not latest_data:
        return None  # Handle the case when there is no data

    # Extract temperature values from the latest data
    latest_data_values = list(latest_data.values())[0]
    live_out_temperature = latest_data_values.get("outside_temperature")
    live_out_hum = latest_data_values.get("outside_humidity")
    live_in_temperature = latest_data_values.get("inside_temperature")
    live_in_hum = latest_data_values.get("inside_humidity")
    live_freq = latest_data_values.get("frequency")

    # Return a dictionary containing the extracted values
    return {
        "live_out_temperature": live_out_temperature,
        "live_out_humidity": live_out_hum,
        "live_in_temperature": live_in_temperature,
        "live_in_humidity": live_in_hum,
        "live_frequency": live_freq
    }

def calculate_harvest():
    # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    harvest_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest 5 records
    latest_data = harvest_ref.order_by_key().limit_to_last(5).get()

    if not latest_data:
        return None  # Handle the case when there is no data

    # Extract temperature values from the dictionary
    temperature_values = [float(value.get("outside_temperature")) for value in latest_data.values()]

    # Calculate average temperature
    if temperature_values:
        average_temperature = sum(temperature_values) / len(temperature_values)
        return average_temperature
    else:
        return None  # Handle the case when there are no temperature values

with open('models/svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    average_freq_value = detect_swarming()
    average_rain_value = feeding_need()
    live_data = get_live_data()

    in_temp = live_data["live_out_temperature"]
    in_hum = live_data["live_out_humidity"]
    freq = live_data["live_frequency"]
    co_level = 300
    
    # Make prediction using the SVM model
    prediction = model.predict([[in_temp,in_hum, co_level,freq]])
  
    

    # if 400 <= average_freq_value <=500:
    #     swarming_alert = True
    # else:
    #     swarming_alert = False

    # Pass swarming_alert to the template
    rounded_average_freq = round(average_freq_value, 3)
    rounded_average_rain = round(average_rain_value, 3)

    return render_template('index.html', swarming_alert=rounded_average_freq, feeding_need=rounded_average_rain, live_data=live_data, prediction= prediction)



@app.route('/api/data', methods=['GET'])
def get_data_api():
    # Retrieving data from readings node
    # Retrieve the latest data (e.g., the last 10 records)
    latest_data = ref.order_by_key().limit_to_last(10).get()

    # Convert the data to an array for easier serialization
    temperature_array = [{"timestamp": key, "outside_temperature": value.get("outside_temperature")} for key, value in latest_data.items()]

    return jsonify({"ssss":  temperature_array})

if __name__ == '__main__':
    app.run(debug=True)
