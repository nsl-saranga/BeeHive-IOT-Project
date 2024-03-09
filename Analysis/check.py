import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Load the dataset
df = pd.read_csv('health_status.csv')

# Extract features and target variable
X = df[['Temperature (Celsius)', 'Humidity (%)', 'Hive Frequency', 'CO2 Concentration (ppm)']]
y = df['Health Status']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Standardize the features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# Create an SVM model with class balancing
svm_model = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')

# Train the model on the training data
svm_model.fit(X_train, y_train)

# Save the trained model to a pickle file
with open('svm_model.pkl', 'wb') as model_file:
    pickle.dump(svm_model, model_file)

# Predict on the testing data
y_pred = svm_model.predict(X_test)

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


y_pred = svm_model.predict([[30.4,59.87,407.35,147.54]])
print(y_pred)

