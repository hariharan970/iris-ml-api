# Iris ML API

Machine Learning REST API for Iris Flower Classification

## Project Overview

This project builds a REST API that uses a machine learning model to classify Iris flowers based on their physical measurements.

The project was developed progressively from a basic machine learning API into a more complete API service with input validation, model integration, testing, security, monitoring, API versioning, Docker containerization, integration testing, load testing, and continuous integration.

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

The goal is to predict the species of an Iris flower from its four physical measurements.

## API Contract

The prediction endpoint accepts four numerical measurements of an Iris flower:

* `sepal_length`
* `sepal_width`
* `petal_length`
* `petal_width`

The API validates the input before passing it to the trained Logistic Regression model.

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
* Integration testing
* Load testing
* GitHub Actions CI

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
  +----> Prometheus Metrics
  |
  +----> Application Logs
  |
  v
JSON Response
  |
  v
Client
```

### Flow Explanation

First, the client sends a prediction request to the FastAPI application.

The API checks the `X-API-Key` header for authentication. After the request passes security checks, Pydantic validates the input data.

Valid measurements are passed to the trained Logistic Regression model. The model predicts the Iris species.

The application records relevant request and prediction information through logging and Prometheus metrics before returning the prediction as a JSON response.

## API Versioning

The API uses versioned routers to organize different API versions.

### Version 1

Version 1 provides the main prediction functionality.

It includes:

* Single prediction
* Batch prediction
* Model information

Example base path:

```text
/api/v1
```

### Version 2

The project also includes a version 2 prediction router.

Example base path:

```text
/api/v2
```

API versioning allows the API to evolve while keeping different versions organized.

## Batch Prediction

The API supports batch prediction so that multiple Iris flower measurements can be submitted in a single request.

Batch requests are validated before being passed to the machine learning model.

The project includes validation handling for:

* Incorrect payload structures
* Invalid input values
* Empty or invalid requests
* Batch requests that are too small
* Batch requests that exceed the configured maximum batch size

## Model Information

The API provides a dedicated model information endpoint.

This allows the running application to expose information about the loaded machine learning model.

## Health Check

A health endpoint is included to verify that the API service is running correctly.

This can be used to check the availability of the application.

## Security

API key authentication was added to protect the prediction endpoints.

Requests use the following HTTP header:

```text
X-API-Key
```

The API rejects requests when the API key is missing or invalid.

The project also includes input validation edge-case handling and CORS configuration.

The API key is managed through environment variables rather than being hard-coded into the application.

## Logging

Structured application logging was added to help monitor API activity and diagnose problems.

The project includes:

* Application logging configuration
* Console logging
* File logging
* Request logging middleware
* Request ID tracking

Request logging helps provide visibility into API requests and responses during development and testing.

## Monitoring

Prometheus monitoring was added using `prometheus-fastapi-instrumentator`.

The API exposes a metrics endpoint:

```text
/metrics
```

A custom Prometheus counter is also used to track Iris predictions:

```text
iris_predictions_total
```

This provides a basic monitoring foundation for observing API activity and prediction counts.

## Testing

The project uses `pytest` and FastAPI `TestClient` for automated testing.

The test suite covers areas including:

* API endpoints
* Prediction functionality
* Input validation
* Batch prediction
* API versioning
* Security
* Error handling
* Health checks
* Model information
* Validation edge cases

The completed test suite contains 13 automated tests.

Integration and load testing were also performed to verify API behavior under multiple requests.

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

Docker Compose can be used to run the API in a containerized environment.

### Running with Docker Compose

Create a local `.env` file from the provided example:

```bash
copy .env.example .env
```

Then start the application:

```bash
docker compose up --build
```

The `.env` file contains local configuration values and is excluded from Git using `.gitignore`.

## Installation

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API documentation can then be accessed through the FastAPI Swagger UI.

```text
http://127.0.0.1:8000/docs
```

The OpenAPI specification is also available through:

```text
http://127.0.0.1:8000/openapi.json
```

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

The workflow provides continuous integration for the project.

It automatically:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs the project dependencies from `requirements.txt`.
4. Runs the complete pytest test suite using `pytest -q`.

The workflow runs when changes are pushed to the `main` branch and when a pull request targets the `main` branch.

This helps detect test failures and regressions after code changes.

## Independent Extension

### GitHub Actions Automated Testing

As an independent extension, GitHub Actions CI was added to automatically run the project's automated tests.

The workflow is defined in:

```text
.github/workflows/tests.yml
```

This extension was independently selected and implemented beyond the scripted project tasks.

It provides continuous automated testing and helps verify that the application continues to pass its test suite when new changes are pushed to the repository.

## Project Structure

```text
iris-ml-api/
│
├── app/
│   ├── routers/
│   │   ├── v1.py
│   │   └── v2.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
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
├── .env.example
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

## Project Development

The project was developed progressively from the initial Iris classification API into a more complete machine learning API service.

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

[GitHub Repository](https://github.com/hariharan970/iris-ml-api)

## Public API

[Live API](https://iris-ml-api-ms1j.onrender.com)
