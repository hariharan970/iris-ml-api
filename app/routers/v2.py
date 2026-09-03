import numpy as np
from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import PredictionInput
from app.exceptions import InvalidInputShapeError


router = APIRouter(prefix="/api/v2")


@router.post("/predict")
def predict_v2(data: PredictionInput, request: Request):
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
        probabilities = request.app.state.model.predict_proba(input_data)[0]

        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[int(prediction[0])]

        return {
            "prediction": predicted_class,
            "probabilities": {
                class_name: float(probability)
                for class_name, probability in zip(class_names, probabilities)
            },
            "model_version": "2.0",
            "request_id": request_id,
        }

    except Exception as e:
        request.app.state.logger.exception(
            "request_id=%s V2 prediction failed: %s",
            request_id,
            e,
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed",
        )
