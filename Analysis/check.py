import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Load the dataset
df = pd.read_csv('hive_health_dataset.csv')

# Extract the 'Timestamp' column and drop it from the features
timestamps = df['Timestamp']
X = df.drop(['Hive Health', 'Timestamp'], axis=1)
y = df['Hive Health']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create an SVM model with class balancing
svm_model = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')

# Train the model on the training data
svm_model.fit(X_train_scaled, y_train)

# Save the trained model to a pickle file
with open('svm_model.pkl', 'wb') as model_file:
    pickle.dump(svm_model, model_file)

# Predict on the testing data
y_pred = svm_model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print the results
print(f'Accuracy: {accuracy:.2f}')
print('\nConfusion Matrix:')
print(conf_matrix)
print('\nClassification Report:')
print(class_report)

targets = {0: 'healthy', 1: 'not healthy'}  # Assuming 'healthy' is 0 and 'not healthy' is 1
print("\nPredicted and True Labels for the first 10 instances:")
for i in range(10):
    predicted_label = y_pred[i]
    actual_label = y_test.iloc[i]
    print(f"Predicted: {predicted_label}, Actual: {actual_label}")
