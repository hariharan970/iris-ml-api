from contextlib import asynccontextmanager
import logging
import uuid

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.models.schemas import PredictionInput


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    model_version: str
    request_id: str


class InvalidInputShapeError(Exception):
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ML model...")
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully!")
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(InvalidInputShapeError)
async def invalid_input_shape_handler(
    request: Request,
    exc: InvalidInputShapeError
):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input shape"}
    )


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


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    request_id = str(uuid.uuid4())

    input_data = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width,
    ]])

    if input_data.shape != (1, 4):
        raise InvalidInputShapeError()

    try:
        prediction = app.state.model.predict(input_data)

        probabilities = app.state.model.predict_proba(input_data)
        confidence = float(np.max(probabilities))

        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[int(prediction[0])]

        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "model_version": "1.0",
            "request_id": request_id
        }

    except Exception as e:
        logger.exception(
            "Prediction failed for request %s: %s",
            request_id,
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )