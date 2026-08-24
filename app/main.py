from contextlib import asynccontextmanager

import joblib
import numpy as np
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ML model...")
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully!")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "ML API is alive"}


@app.post("/predict")
def predict():
    features = {
        "sepal_length": 6.5,
        "sepal_width": 3.0,
        "petal_length": 5.5,
        "petal_width": 1.8,
    }

    input_data = np.array([[
        features["sepal_length"],
        features["sepal_width"],
        features["petal_length"],
        features["petal_width"],
    ]])

    prediction = app.state.model.predict(input_data)

    return {
        "prediction": prediction[0].item()
    }