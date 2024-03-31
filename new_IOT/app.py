from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import db, credentials
import math
import pickle
import json
from datetime import datetime
import math
import experiment  # experiment data for daily yield. 

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
    live_co = latest_data_values.get("co")
    live_weight = latest_data_values.get("weight")
    live_rain = latest_data_values.get("rainfall")

    # Return a dictionary containing the extracted values
    return {
        "live_out_temperature": live_out_temperature,
        "live_out_humidity": live_out_hum,
        "live_in_temperature": live_in_temperature,
        "live_in_humidity": live_in_hum,
        "live_frequency": live_freq,
        "live_co": live_co,
        "live_weight": live_weight,
        "live_rain": live_rain
    }


def calculate_harvest():
    # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    harvest_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest 5 records
    latest_data = harvest_ref.order_by_key().limit_to_last(5).get()

    if not latest_data:
        return None  # Handle the case when there is no data

    # Extract weight values from the dictionary
    weight_values = [float(value.get("weight")) for value in latest_data.values()]

    # Calculate average weight
    if weight_values:
        average_weight = sum(weight_values) / len(weight_values)
        return average_weight
    else:
        return None  # Handle the case when there are no temperature values



def calculate_extreme():
     # Assuming the data is stored in '/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings'
    harvest_ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

    # Retrieve the latest 5 records
    latest_data = harvest_ref.order_by_key().limit_to_last(5).get()

    if not latest_data:
        return None  # Handle the case when there is no data

    # Extract weight values from the dictionary
    temp_values = [float(value.get("outside_temperature")) for value in latest_data.values()]

    # Calculate average weight
    if temp_values:
        average_temp = sum(temp_values) / len(temp_values)
        return average_temp
    else:
        return None  # Handle the case when there are no temperature values



with open('models/svm_model.pkl', 'rb') as f:
    model = pickle.load(f)


def get_graph_data():
  # Retrieve the latest data (e.g., the last 10 records)
    latest_data = ref.order_by_key().limit_to_last(15).get()

    # Convert the data to an array for easier serialization
    array = [{"timestamp": key, "outside_temperature": value.get("outside_temperature"), "inside_temperature": value.get("inside_temperature"),"outside_humidity": value.get("outside_humidity"),"inside_humidity": value.get("inside_humidity"),"frequency": value.get("frequency"),"weight": value.get("weight"),"co2": value.get("co")} for key, value in latest_data.items()]

    return (array)

def daily_yield():
    data = experiment.get_data()
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
            data_dict['average_afternoon_temperature'] = round(sum(afternoon_temperature) / len(afternoon_temperature), 3)
        else:
            data_dict['average_afternoon_temperature'] = None

        if afternoon_humidity:
            data_dict['average_afternoon_humidity'] = round(sum(afternoon_humidity) / len(afternoon_humidity), 3)
        else:
            data_dict['average_afternoon_humidity'] = None

        if afternoon_rainfall:
            data_dict['average_afternoon_rainfall'] = round(sum(afternoon_rainfall) / len(afternoon_rainfall), 3)
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
    average_harvest_value = calculate_harvest()
    extreme_temp_value = calculate_extreme()

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

    return render_template('index.html', harvest_alert=average_harvest_value, extreme_alert=extreme_temp_value, swarming_alert=rounded_average_freq, feeding_need=rounded_average_rain, live_data=live_data, prediction= prediction)

@app.route('/HiveStats')
def page1():
    graph_data = get_graph_data()
    return render_template('hiveStats.html', graph_data = graph_data)

@app.route('/DailyYield')
def page2():
    honey = daily_yield()
    return render_template('dailyYield.html',honey=honey)

@app.route('/api/live_data', methods=['GET'])
def get_live_data_api():
    # Retrieve live data
    latest_data = get_live_data()  # Assuming this function retrieves live data
    
    # Convert the dictionary to JSON
    json_data = jsonify(latest_data)
    
    # Return the JSON data
    return json_data

@app.route('/api/timely_data', methods=['GET'])
def get_timely_data_api():
    # Retrieve graph data
    graph_data = get_graph_data()  # Assuming this function retrieves graph data
    
    # Convert the dictionary to JSON
    json_data = jsonify(graph_data)
    
    # Return the JSON data
    return json_data
    

if __name__ == '__main__':
    app.run(debug=True)
