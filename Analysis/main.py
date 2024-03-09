import pickle

with open('svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Print the input features to check their values
input_features = [[33.95,51.81,434.43,147.37]]
print("Input Features:", input_features)

# Make the prediction
prediction = model.predict(input_features)

# Print the raw prediction values or any intermediate steps for debugging
print("Raw Prediction:", prediction)

# Print the final prediction after any post-processing (if applicable)
print("Final Prediction:", prediction)
