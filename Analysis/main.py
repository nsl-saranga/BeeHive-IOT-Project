import firebase_admin
from firebase_admin import db, credentials
from datetime import datetime
import numpy as np
import pickle
from sklearn.impute import SimpleImputer

# Authenticate to Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://bees-9478f-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Creating reference to readings node
ref = db.reference("/UsersData/X3dJJfbdJGRYA9WcYi7dun8I0cp2/readings")

# Retrieving data from readings node
data = ref.get()

# Convert timestamps to human-readable format
if data:
    for reading_id, reading_data in data.items():
        timestamp = int(reading_data.get("timestamp", 0))
        readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        reading_data["readable_time"] = readable_time

    # Get the values to numpy arrays
    timestamps = np.array([datetime.strptime(reading_data['readable_time'], '%Y-%m-%d %H:%M:%S') for reading_data in data.values()])
    humidity_array = np.array([float(reading_data['humidity']) for reading_data in data.values()])
    temperature_array = np.array([float(reading_data['temperature']) for reading_data in data.values()])
    frequency_array = np.array([float(reading_data['frequency']) for reading_data in data.values()])

    # Replace NaN values with a default value, e.g., -1
    humidity_array[np.isnan(humidity_array)] = -1
    temperature_array[np.isnan(temperature_array)] = -1
    frequency_array[np.isnan(frequency_array)] = -1

    # Impute missing values using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    humidity_array = imputer.fit_transform(humidity_array.reshape(-1, 1)).reshape(-1)
    temperature_array = imputer.fit_transform(temperature_array.reshape(-1, 1)).reshape(-1)
    frequency_array = imputer.fit_transform(frequency_array.reshape(-1, 1)).reshape(-1)

    # Load the pre-trained model using pickle
    with open('svm_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    # Reshape arrays for prediction
    data_array = np.column_stack((humidity_array, temperature_array, frequency_array))

    # Assuming 0 for the missing features
    missing_features = np.zeros(( data_array.shape[0], 6 -  data_array.shape[1]))

    # Concatenate the missing features to the existing ones
    data_array = np.hstack(( data_array, missing_features))

    # Now 'loaded_model' can be used for predictions
    predictions = loaded_model.predict(data_array)

    # Print temperature, humidity, date, and predicted result all together
    for timestamp, humidity, temperature, frequency, prediction in zip(timestamps, humidity_array, temperature_array, frequency_array, predictions):
        print(f"Date: {timestamp}, Humidity: {humidity}, Temperature: {temperature}, Frequency: {frequency} Predicted Result: {prediction}")

else:
    print("No data found.")
