import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Number of data points
num_samples = 1000

# Generate synthetic data for temperature, humidity, frequency, CO2 level, and sound intensity
temperature = np.random.uniform(30, 40, num_samples)
humidity = np.random.uniform(40, 80, num_samples)
frequency = np.random.uniform(80, 120, num_samples)
co2_level = np.random.uniform(300, 500, num_samples)
sound_intensity = np.random.uniform(60, 90, num_samples)

# Assume a simple relationship between features and health status
# Adjust this based on the characteristics you want in your synthetic data
health_status = np.where(
    (temperature > 35) & (humidity > 50) & (frequency > 90) & (co2_level < 450) & (sound_intensity > 70),
    1, 0
)

# Randomly select some instances with health_status = 1 to balance the classes
indices_positive_class = np.where(health_status == 1)[0]
num_samples_positive_class = int(0.5 * num_samples)  # Assuming a 50-50 balance

# Create a DataFrame
synthetic_data = pd.DataFrame({
    'Temperature': temperature,
    'Humidity': humidity,
    'Frequency': frequency,
    'CO2 Level': co2_level,
    'Sound Intensity': sound_intensity,
    'Hive Health': 0  # Initialize with all 0s
})

# If there are not enough instances with health_status = 1, adjust the number of samples
if len(indices_positive_class) < num_samples_positive_class:
    num_samples_positive_class = len(indices_positive_class)

# Update health_status for the selected positive class instances
selected_indices_positive_class = np.random.choice(indices_positive_class, num_samples_positive_class, replace=True)
synthetic_data.loc[selected_indices_positive_class, 'Hive Health'] = 1

# Save the synthetic data to a CSV file
synthetic_data.to_csv('synthetic_hive_data.csv', index=False)
