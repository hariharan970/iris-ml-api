import numpy as np
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.models.schemas import PredictionInput
from app.exceptions import InvalidInputShapeError


router = APIRouter(prefix="/api/v1")


class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    model_version: str
    request_id: str


@router.get("/health")
def health(request: Request):
    model_loaded = (
        hasattr(request.app.state, "model")
        and request.app.state.model is not None
    )

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):
    request_id = request.state.request_id

    input_data = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width,
    ]])

    if input_data.shape != (1, 4):
        raise InvalidInputShapeError()

    try:
        prediction = request.app.state.model.predict(input_data)

        probabilities = request.app.state.model.predict_proba(input_data)
        confidence = float(np.max(probabilities))

        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[int(prediction[0])]

        request.app.state.logger.info(
            "request_id=%s Prediction successful: %s",
            request_id,
            predicted_class
        )

        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "model_version": "1.0",
            "request_id": request_id
        }

    except Exception as e:
        request.app.state.logger.exception(
            "request_id=%s Prediction failed: %s",
            request_id,
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


# Task 10 - API Versioning:
# If we create /api/v2/predict later, we can create a separate
# v2 router and a new Pydantic response schema.
# The v1 API will remain unchanged, while v2 can return
# additional fields without breaking existing v1 clients.