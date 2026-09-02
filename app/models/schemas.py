from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    model_version: str
    request_id: str


class PredictionBatchInput(BaseModel):
    inputs: list[PredictionInput] = Field(
        ...,
        min_length=1,
        max_length=100
    )


class PredictionBatchOutput(BaseModel):
    predictions: list[PredictionOutput]