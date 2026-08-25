from contextlib import asynccontextmanager
import uuid

import joblib
import numpy as np
from fastapi import FastAPI

from app.models.schemas import PredictionInput


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


@app.get("/health")
def health():
    model_loaded = hasattr(app.state, "model") and app.state.model is not None

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }


@app.post("/predict")
def predict(data: PredictionInput):
    input_data = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width,
    ]])

    prediction = app.state.model.predict(input_data)

    probabilities = app.state.model.predict_proba(input_data)
    confidence = float(np.max(probabilities))

    class_names = ["setosa", "versicolor", "virginica"]
    predicted_class = class_names[prediction[0]]

    request_id = str(uuid.uuid4())

    return {
        "prediction": predicted_class,
        "confidence": confidence,
        "request_id": request_id
    }