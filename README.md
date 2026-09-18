# Iris ML API

Machine Learning REST API for Iris Flower Classification

## Project Overview

This project builds a REST API that uses a machine learning model to classify Iris flowers based on their physical measurements. The main purpose of the project is to learn how to integrate a machine learning model into a Python API and expose its predictions through REST endpoints.

The project was developed progressively with API validation, model integration, testing, security, monitoring, API versioning, Docker containerization, and deployment-related work.

## Dataset

The project uses the built-in Iris dataset provided by `scikit-learn`.

The dataset contains four input features:

* Sepal length
* Sepal width
* Petal length
* Petal width

The model classifies each flower into one of three species:

* Setosa
* Versicolor
* Virginica

## Machine Learning Problem

This is a **supervised classification problem**.

The selected machine learning algorithm is **Logistic Regression**.

The goal is to predict the species of an Iris flower from its four measurements.

## API Contract

The prediction endpoint accepts four numerical measurements of an Iris flower: sepal length, sepal width, petal length, and petal width. The API validates the input before passing it to the trained Logistic Regression model.

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

## API Features

The completed API includes:

* FastAPI REST API
* Pydantic request validation
* Machine learning model loading
* API versioning
* Single prediction endpoint
* Batch prediction endpoint
* Model information endpoint
* Health endpoint
* Structured logging
* Request logging middleware
* Centralized configuration using environment variables
* API key authentication using the `X-API-Key` header
* CORS configuration
* Prometheus metrics
* Custom prediction counter metric
* Automated pytest test suite
* Docker containerization
* Docker Compose configuration
* Integration and load testing

## Request Flow

```text
Client
  |
  | Prediction request
  v
FastAPI Application
  |
  v
API Key Security
  |
  v
Input Validation
  |
  v
Machine Learning Model
  |
  v
Prediction
  |
  v
Prometheus Metrics / Logging
  |
  v
JSON Response
  |
  v
Client
```

## API Versioning

The API uses versioned routers.

### Version 1

The version 1 API provides the main prediction functionality, including batch prediction and model information functionality.

### Version 2

The project also includes an `/api/v2` router for versioned prediction functionality.

## Batch Prediction

The API supports batch prediction so that multiple Iris flower measurements can be submitted in a single request.

Batch requests are validated before being passed to the model.

The project also includes validation handling for incorrect payload shapes and batch-size edge cases.

## Model Information

The API provides model information through a dedicated endpoint. This allows the running application to expose information about the loaded machine learning model.

## Security

API key authentication was added to protect prediction endpoints.

Requests use the following HTTP header:

```text
X-API-Key
```

The API rejects requests when the API key is missing or invalid.

The API also includes validation edge-case handling and CORS configuration.

## Logging

Structured application logging was added to help monitor API activity and diagnose problems.

The project includes:

* Application logging configuration
* Console logging
* File logging
* Request logging middleware

## Monitoring

Prometheus monitoring was added using `prometheus-fastapi-instrumentator`.

The API exposes:

```text
/metrics
```

A custom Prometheus counter is also used to track Iris predictions:

```text
iris_predictions_total
```

This provides a basic monitoring foundation for the API.

## Testing

The project uses `pytest` and FastAPI `TestClient` for automated testing.

The test suite covers areas including:

* API endpoints
* Prediction functionality
* Validation
* API versioning
* Security
* Error handling

Integration and load testing were also performed.

### Load Test Results

A load test of 50 requests completed with:

```text
Successful requests: 50
Failed requests: 0
Total test time: 0.291 seconds
Average response: 0.217 seconds
Max response: 0.263 seconds
Min response: 0.155 seconds
```

A load test of 200 requests completed with:

```text
Successful requests: 200
Failed requests: 0
Total test time: 1.536 seconds
Average response: 1.059 seconds
Max response: 1.303 seconds
Min response: 0.560 seconds
```

## Docker

The API was containerized using Docker.

The project includes:

* `Dockerfile`
* `docker-compose.yml`

Docker Compose can be used to run the application in a containerized environment.

## Project Structure

```text
iris-ml-api/
│
├── app/
│   ├── routers/
│   │   ├── v1.py
│   │   └── v2.py
│   ├── models/
│   │   └── schemas.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── metrics.py
│   └── security.py
│
├── ml/
│   └── saved_model/
│       └── model.joblib
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Technology Stack

* Python
* FastAPI
* Scikit-learn
* Pydantic
* Uvicorn
* Pytest
* Prometheus
* Docker
* Docker Compose
* Git
* GitHub
* GitHub Actions

## Installation

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the API


For the independent extension, I chose to add **GitHub Actions CI** so that the project's automated tests run automatically whenever the code changes.

Start the FastAPI application with Uvicorn:
 22146d7 (docs: update README with independent extension)

```bash
uvicorn app.main:app --reload
```

The API documentation can then be accessed through the FastAPI Swagger UI.

## Running Tests

Run the complete test suite with:

```bash
pytest -q
```

## GitHub Actions

The project includes a GitHub Actions workflow located at:

```text
.github/workflows/tests.yml
```


The workflow runs automatically on:

The workflow automatically:
 22146d7 (docs: update README with independent extension)

1. Checks out the repository.
2. Sets up Python.
3. Installs the dependencies from `requirements.txt`.
4. Runs the pytest test suite.


It performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs the dependencies from `requirements.txt`.
4. Runs the complete pytest suite with `pytest -q`.

This extension was independently selected and implemented beyond the scripted project tasks. It provides continuous automated testing and helps detect regressions after code changes.

The workflow runs for pushes to the `main` branch and for pull requests targeting `main`.
 22146d7 (docs: update README with independent extension)

## Independent Extension

### GitHub Actions Automated Testing

As an independent extension, GitHub Actions was added to automatically run the project's pytest test suite.

The workflow is defined in:

```text
.github/workflows/tests.yml
```

It automatically installs the project dependencies and executes the tests whenever changes are pushed to the `main` branch or when a pull request targets `main`.

This extension was independently selected and implemented beyond the scripted project tasks. It provides continuous automated testing and helps detect regressions when new changes are pushed to the repository.

## Project Development

The project was developed progressively from the initial Iris classification API into a more complete ML API service.

The development covered:

1. Project and API planning
2. Python environment setup
3. Machine learning model training and saving
4. FastAPI application development
5. Model loading
6. Input validation
7. Prediction endpoints
8. Response models and error handling
9. Structured logging
10. API versioning
11. Batch prediction and model information
12. Configuration management
13. Automated testing
14. API v2 development
15. Docker containerization
16. Docker Compose
17. API security
18. Prometheus monitoring and metrics
19. Integration and load testing
20. Final polishing and independent extension

## Repository

https://github.com/hariharan970/iris-ml-api

## Public API

https://iris-ml-api-ms1j.onrender.com