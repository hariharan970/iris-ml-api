import json
import time

import numpy as np
from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput,
)
from app.exceptions import InvalidInputShapeError


router = APIRouter(prefix="/api/v1")


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


@router.post(
    "/predict-batch",
    response_model=PredictionBatchOutput
)
def predict_batch(
    data: PredictionBatchInput,
    request: Request
):
    request_id = request.state.request_id
    start_time = time.time()

    batch_size = len(data.inputs)

    try:
        # Create one NumPy array for the entire batch
        input_data = np.array([
            [
                item.sepal_length,
                item.sepal_width,
                item.petal_length,
                item.petal_width,
            ]
            for item in data.inputs
        ])

        if input_data.shape != (batch_size, 4):
            raise InvalidInputShapeError()

        # Predict the entire batch at once
        predictions = request.app.state.model.predict(input_data)

        # Get probabilities for the entire batch at once
        probabilities = request.app.state.model.predict_proba(input_data)

        class_names = ["setosa", "versicolor", "virginica"]

        results = []

        # Format the predictions after model inference
        for index, prediction in enumerate(predictions):
            predicted_class = class_names[int(prediction)]
            confidence = float(np.max(probabilities[index]))

            results.append(
                PredictionOutput(
                    prediction=predicted_class,
                    confidence=confidence,
                    model_version="1.0",
                    request_id=request_id
                )
            )

        duration = (time.time() - start_time) * 1000

        request.app.state.logger.info(
            "request_id=%s batch_size=%s "
            "batch_prediction_successful duration=%.2fms",
            request_id,
            batch_size,
            duration
        )

        return PredictionBatchOutput(
            predictions=results
        )

    except InvalidInputShapeError:
        raise

    except Exception as e:
        duration = (time.time() - start_time) * 1000

        request.app.state.logger.exception(
            "request_id=%s batch_size=%s "
            "Batch prediction failed duration=%.2fms error=%s",
            request_id,
            batch_size,
            duration,
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )


@router.get("/model-info")
def model_info(request: Request):
    metadata_path = "ml/saved_model/model_metadata.json"

    try:
        with open(metadata_path, "r") as file:
            metadata = json.load(file)

        request.app.state.logger.info(
            "request_id=%s Model metadata retrieved",
            request.state.request_id
        )

        return metadata

    except Exception as e:
        request.app.state.logger.exception(
            "request_id=%s Failed to load model metadata: %s",
            request.state.request_id,
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Model metadata unavailable"
        )