from pydantic import BaseModel, ConfigDict, Field


class PredictionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sepal_length: float = Field(..., gt=0, le=10)
    sepal_width: float = Field(..., gt=0, le=10)
    petal_length: float = Field(..., gt=0, le=10)
    petal_width: float = Field(..., gt=0, le=10)


class PredictionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: str
    confidence: float
    model_version: str
    request_id: str


class PredictionBatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inputs: list[PredictionInput] = Field(
        ...,
        min_length=1,
        max_length=100
    )


class PredictionBatchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predictions: list[PredictionOutput]