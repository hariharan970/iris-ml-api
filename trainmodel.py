import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

# Load Iris dataset
iris = load_iris()

# Train model
model = LogisticRegression(max_iter=200)
model.fit(iris.data, iris.target)

# Save trained model
joblib.dump(model, "model.joblib")

print("Model saved successfully!")