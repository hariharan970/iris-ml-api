import joblib


# Load the saved model
model = joblib.load("ml/saved_model/model.joblib")


# Example Iris flower measurements
sample = [[5.1, 3.5, 1.4, 0.2]]


# Make prediction
prediction = model.predict(sample)


# Convert numeric prediction to flower name
flower_names = ["setosa", "versicolor", "virginica"]

predicted_flower = flower_names[prediction[0]]

print(f"Predicted flower: {predicted_flower}")