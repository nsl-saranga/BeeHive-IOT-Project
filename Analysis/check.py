from datetime import datetime

data = {
    'UsersData': {
        'X3dJJfbdJGRYA9WcYi7dun8I0cp2': {
            'readings': {
                '1708382187': {'frequency': '60.30', 'humidity': '60.00', 'rainfall': '100', 'temperature': '25.50', 'timestamp': '1708382187'},
                '1708382292': {'frequency': 'nan', 'humidity': '60.00', 'rainfall': '100', 'temperature': '25.50', 'timestamp': '1708382292'},
                # ... (other readings)
            }
        }
    }
}

for user_id, user_data in data['UsersData'].items():
    for reading_id, reading_data in user_data['readings'].items():
        timestamp = int(reading_data['timestamp'])
        readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        reading_data['readable_time'] = readable_time

# Now the 'readable_time' field is added to each reading in the data
print(data)
