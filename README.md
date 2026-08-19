# iris-ml-api
Machine Learning REST API for Iris Flower Classification
# Iris ML API

## Project Overview

This project will build a REST API that uses a machine learning model to classify Iris flowers based on their physical measurements. The main purpose of the project is to learn how to integrate a machine learning model into a Python API and expose its predictions through a REST endpoint.

## Dataset

The project uses the built-in Iris dataset provided by `scikit-learn`.

The dataset contains four input features:

* Sepal length
* Sepal width
* Petal length
* Petal width

The model will classify each flower into one of three species:

* Setosa
* Versicolor
* Virginica

## Machine Learning Problem

This is a **supervised classification problem**.

The selected machine learning algorithm is **Logistic Regression**.

The goal is to predict the species of an Iris flower from its four measurements.

## API Contract

The `/predict` endpoint accepts four numerical measurements of an Iris flower: sepal length, sepal width, petal length, and petal width. The API validates that all required values are provided and are valid numbers. After validation, the values are passed to the trained Logistic Regression model, which predicts whether the flower is Setosa, Versicolor, or Virginica. The API then returns the predicted species as a JSON response. Invalid or missing input will result in a validation error rather than a prediction.

### Endpoint

`POST /predict`

### Example Input

```json
{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```

### Example Output

```json
{
    "prediction": "setosa"
}
```

## Request Flow

```text
Client
  |
  | POST /predict
  | Flower measurements
  ↓
FastAPI Endpoint
  |
  ↓
Input Validation
  |
  ↓
Logistic Regression Model
  |
  ↓
Prediction
  |
  ↓
JSON Response
  |
  ↓
Client
```

### Flow Explanation

First, the client sends the four Iris flower measurements to the `/predict` endpoint. FastAPI receives the request and validates the input. If the input is valid, the measurements are passed to the trained Logistic Regression model. The model predicts the flower species. Finally, the API returns the prediction to the client in JSON format.

## Project Scope

The initial version will focus on one prediction endpoint. The main goal is to understand API development, input validation, machine learning model integration, testing, and deployment.

Complex machine learning techniques are intentionally avoided because the main focus of this project is backend and ML API engineering.

## Planned Development

1. Set up the Python environment.
2. Create the project folder structure.
3. Load and train the Iris classification model.
4. Save the trained model.
5. Build the FastAPI application.
6. Add request validation.
7. Implement the `/predict` endpoint.
8. Test the API.
9. Containerize the application.
10. Deploy the API.

## Technology Stack

* Python
* FastAPI
* Scikit-learn
* Pydantic
* Uvicorn
* Git
* GitHub

## Day 1 Goal

The dataset, machine learning problem, API contract, and initial architecture have been defined before implementation begins.
