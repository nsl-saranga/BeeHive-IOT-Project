import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Number of rows in the dataset
num_rows = 1000

# Generate timestamp starting from a specific date and time
start_time = datetime(2024, 3, 9, 8, 0, 0)
timestamps = [start_time + timedelta(hours=i) for i in range(num_rows)]

# Generate random data within specified ranges, rounded to 2 decimal points
temperature = np.round(np.random.uniform(28, 35, num_rows), 2)
humidity = np.round(np.random.uniform(50, 60, num_rows), 2)
co2_concentration = np.round(np.random.uniform(390, 450, num_rows), 2)
hive_frequency = np.round(np.random.normal(150, 5, num_rows), 2)

# Create a DataFrame
data = {
    'Timestamp': timestamps,
    'Temperature (Celsius)': temperature,
    'Humidity (%)': humidity,
    'CO2 Concentration (ppm)': co2_concentration,
    'Hive Frequency': hive_frequency
}

df = pd.DataFrame(data)
df['Health Status'] = 'Healthy'

# Set seed for reproducibility
np.random.seed(42)

# Number of rows in the dataset
num_rows = 1000

# Generate timestamp starting from a specific date and time
start_time = datetime(2024, 3, 9, 8, 0, 0)
timestamps = [start_time + timedelta(hours=i) for i in range(num_rows)]

# Generate random data with abnormal conditions, rounded to 2 decimal points
temperature = np.concatenate([np.round(np.random.uniform(10, 27.9, num_rows // 2), 2),
                              np.round(np.random.uniform(35.1, 40, num_rows // 2), 2)])
humidity = np.concatenate([np.round(np.random.uniform(30, 49.9, num_rows // 2), 2),
                           np.round(np.random.uniform(60.1, 80, num_rows // 2), 2)])
co2_concentration = np.round(np.random.uniform(450, 800, num_rows), 2)
hive_frequency = np.concatenate([np.round(np.random.normal(180, 20, num_rows // 2), 2),
                                 np.round(np.random.normal(210, 30, num_rows // 2), 2)])

# Create a DataFrame
data = {
    'Timestamp': timestamps,
    'Temperature (Celsius)': temperature,
    'Humidity (%)': humidity,
    'CO2 Concentration (ppm)': co2_concentration,
    'Hive Frequency': hive_frequency
}

unhealthy_df = pd.DataFrame(data)
unhealthy_df['Health Status'] = 'Unhealthy'
result_df = pd.concat([df, unhealthy_df], ignore_index=True)

# Shuffle the rows of the DataFrame
shuffled_df = result_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Display the shuffled DataFrame
print(shuffled_df)

csv_file_path = 'health_status.csv'

# Write the DataFrame to a CSV file
shuffled_df.to_csv(csv_file_path, index=False)
