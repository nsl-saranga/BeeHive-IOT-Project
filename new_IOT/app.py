from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import db, credentials
import math
import pickle
import json
from datetime import datetime
import math

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

    # Retrieve the latest 10 records
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

def get_graph_data():
  # Retrieve the latest data (e.g., the last 10 records)
    latest_data = ref.order_by_key().limit_to_last(10).get()

    # Convert the data to an array for easier serialization
    array = [{"timestamp": key, "outside_temperature": value.get("outside_temperature"),"outside_humidity": value.get("outside_humidity"),"frequency": value.get("frequency")} for key, value in latest_data.items()]

    return (array)

def daily_yeield():
  
    data = [
    ("2024-03-13 05:00:00", 42.5, 20, 60, 15),  # (Timestamp, Weight, Rainfall, Outside Humidity, Outside Temperature)
    ("2024-03-13 05:30:00", 42.7, 20, 62, 15),
    ("2024-03-13 06:00:00", 43.0, 20, 64, 16),
    ("2024-03-13 06:30:00", 43.3, 20, 65, 16),
    ("2024-03-13 07:00:00", 43.5, 20, 66, 17),
    ("2024-03-13 07:30:00", 43.7, 20, 67, 17),
    ("2024-03-13 08:00:00", 44.0, 20, 68, 18),
    ("2024-03-13 08:30:00", math.nan, 20, 69, 18),  # Example NaN value
    ("2024-03-13 09:00:00", 44.5, 20, 70, 19),
    ("2024-03-13 09:30:00", 44.8, 20, 71, 19),
    ("2024-03-13 10:00:00", 45.0, 20, 72, 20),
    ("2024-03-13 10:30:00", 45.2, 20, 73, 20),
    ("2024-03-13 11:00:00", 45.5, 20, 74, 21),
    ("2024-03-13 11:30:00", 45.8, 20, 75, 21),
    ("2024-03-13 12:00:00", 46.0, 20, 76, 22),
    ("2024-03-13 12:30:00", 46.2, 20, 77, 22),
    ("2024-03-13 13:00:00", 46.5, 20, 78, 23),
    ("2024-03-13 13:30:00", 46.8, 20, 79, 23),
    ("2024-03-13 14:00:00", 47.0, 20, 80, 24),
    ("2024-03-13 14:30:00", 47.2, 20, 81, 24),
    ("2024-03-13 15:00:00", 47.5, 20, 82, 25),
    ("2024-03-13 15:30:00", 47.8, 20, 83, 25),
    ("2024-03-13 16:00:00", 48.0, 20, 84, 26),
    ("2024-03-13 16:30:00", 48.2, 20, 85, 26),
    ("2024-03-13 17:00:00", 48.5, 20, 86, 27),
    ("2024-03-13 17:30:00", 48.7, 20, 87, 27),
    ("2024-03-13 18:00:00", 49.0, 20, 88, 28),
    ("2024-03-13 18:30:00", 49.2, 20, 89, 28),
    ("2024-03-13 19:00:00", 49.5, 20, 90, 29),
    ("2024-03-13 19:30:00", 49.8, 20, 91, 29)
    ]

    daily_data = {}

    for timestamp, weight, rainfall, humidity, temperature in data:
        date = timestamp.split()[0]

        # Filter out NaN values for weight
        if not math.isnan(weight):
            if date not in daily_data:
                daily_data[date] = {'morning_weight': None, 'evening_weight': None, 'afternoon_temperature': [], 'afternoon_humidity': [], 'afternoon_rainfall': []}

            hour = int(timestamp.split()[1].split(":")[0])
            
            # Check if morning weight
            if hour < 6:
                daily_data[date]['morning_weight'] = weight
            # Check if evening weight
            elif hour >= 18:
                daily_data[date]['evening_weight'] = weight
            # Collect afternoon data
            elif 12 <= hour < 18:
                daily_data[date]['afternoon_temperature'].append(temperature)
                daily_data[date]['afternoon_humidity'].append(humidity)
                daily_data[date]['afternoon_rainfall'].append(rainfall)

    # Calculate weight differences and average afternoon values
    for date, data_dict in daily_data.items():
        morning_weight = data_dict['morning_weight']
        evening_weight = data_dict['evening_weight']

        if morning_weight is not None and evening_weight is not None:
            data_dict['weight_difference'] = evening_weight - morning_weight
        else:
            data_dict['weight_difference'] = None

        afternoon_temperature = data_dict['afternoon_temperature']
        afternoon_humidity = data_dict['afternoon_humidity']
        afternoon_rainfall = data_dict['afternoon_rainfall']

        if afternoon_temperature:
            data_dict['average_afternoon_temperature'] = sum(afternoon_temperature) / len(afternoon_temperature)
        else:
            data_dict['average_afternoon_temperature'] = None

        if afternoon_humidity:
            data_dict['average_afternoon_humidity'] = sum(afternoon_humidity) / len(afternoon_humidity)
        else:
            data_dict['average_afternoon_humidity'] = None

        if afternoon_rainfall:
            data_dict['average_afternoon_rainfall'] = sum(afternoon_rainfall) / len(afternoon_rainfall)
        else:
            data_dict['average_afternoon_rainfall'] = None

        # Remove the lists to clean up the data structure
        del data_dict['afternoon_temperature']
        del data_dict['afternoon_humidity']
        del data_dict['afternoon_rainfall']

    return daily_data

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

@app.route('/HiveStats')
def page1():
    graph_data = get_graph_data()
    return render_template('hiveStats.html', graph_data = graph_data)

@app.route('/DailyYield')
def page2():
    honey = daily_yeield()
    return render_template('dailyYield.html',honey=honey)

@app.route('/api/data', methods=['GET'])
def get_data_api():
    # Retrieving data from readings node
    # Retrieve the latest data (e.g., the last 10 records)
    latest_data = ref.order_by_key().limit_to_last(10).get()

    # Convert the data to an array for easier serialization
    temperature_array = [{"timestamp": key, "outside_temperature": value.get("outside_temperature")} for key, value in latest_data.items()]

    return jsonify({temperature_array})

if __name__ == '__main__':
    app.run(debug=True)
