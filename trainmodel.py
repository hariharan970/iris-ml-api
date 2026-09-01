import json
from datetime import date

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


# Load Iris dataset
iris = load_iris()


# Train model
model = LogisticRegression(max_iter=200)
model.fit(iris.data, iris.target)


# Save model
model_path = "ml/saved_model/model.joblib"
joblib.dump(model, model_path)


# Save model metadata
metadata = {
    "model_type": type(model).__name__,
    "version": "1.0",
    "training_date": date.today().isoformat(),
    "expected_features": [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]
}

metadata_path = "ml/saved_model/model_metadata.json"

with open(metadata_path, "w") as file:
    json.dump(metadata, file, indent=4)


print("Model saved successfully!")
print("Metadata saved successfully!")