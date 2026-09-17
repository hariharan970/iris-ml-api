# Iris ML API

A Dockerized FastAPI REST API for Iris flower classification using a trained scikit-learn Logistic Regression model.

## Project Overview

The service accepts four Iris flower measurements and predicts one of three classes: `setosa`, `versicolor`, or `virginica`.

The project progressed from model training and API validation to versioned endpoints, structured logging, configuration management, automated testing, Docker/Compose, API-key security, Prometheus metrics, load testing, and cloud deployment.

## Features

- Logistic Regression model trained on the scikit-learn Iris dataset
- FastAPI REST API with Pydantic validation
- Versioned prediction endpoints (`v1` and `v2`)
- Batch prediction with configurable maximum batch size
- Model metadata endpoint
- API-key protection using `X-API-Key`
- Request IDs and structured request logging
- Prometheus monitoring at `/metrics`
- Docker and Docker Compose support
- Automated pytest suite
- GitHub Actions CI on pushes to `main` and pull requests
- Public deployment on Render

## Architecture

```text
                         +----------------------+
                         |      Client / curl   |
                         +----------+-----------+
                                    |
                                    | HTTP request
                                    v
                         +----------------------+
                         |   Docker Container    |
                         |      FastAPI app     |
                         +----------+-----------+
                                    |
                     +--------------+--------------+
                     |                             |
                     v                             v
             +---------------+              +---------------+
             | API Key Check |              | Request Logger|
             +-------+-------+              +-------+-------+
                     |                              |
                     v                              v
             +---------------+              +---------------+
             | Pydantic      |              | Request ID    |
             | Validation    |              | + timing      |
             +-------+-------+              +---------------+
                     |
                     v
             +-----------------------------+
             | Versioned API Router        |
             | v1 / v2 / batch / metadata  |
             +--------------+--------------+
                            |
                            v
             +-----------------------------+
             | Loaded scikit-learn Model   |
             | Logistic Regression         |
             +--------------+--------------+
                            |
                            v
                   +------------------+
                   | JSON prediction  |
                   +------------------+

        Prometheus instrumentation -> /metrics
        Logs -> console + logs/app.log
```

## Request Flow

1. The client sends an HTTP request to the FastAPI service.
2. Request middleware creates a unique request ID and records request timing.
3. Protected endpoints validate the `X-API-Key` header.
4. Pydantic validates the request body.
5. The selected API router processes the request.
6. The persisted Logistic Regression model is loaded during application startup.
7. The model returns the predicted class and probabilities.
8. The API returns the prediction as a JSON response.
9. Prometheus instrumentation records HTTP metrics.
10. The custom `iris_predictions_total` counter tracks successful predictions by class.

## Dataset and Model

The project uses the built-in Iris dataset from scikit-learn.

### Input Features

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

### Output Classes

- `setosa`
- `versicolor`
- `virginica`

### Algorithm

**Logistic Regression**

The trained model is stored at:

```text
ml/saved_model/model.joblib
```

Model metadata is stored at:

```text
ml/saved_model/model_metadata.json
```

## API Endpoints

### GET `/`

Basic service response.

Local:

```bash
curl http://localhost:8000/
```

Public:

```text
https://iris-ml-api-ms1j.onrender.com/
```

Example response:

```json
{"message":"ML API is alive"}
```

### GET `/api/v1/health`

Returns service and model-loading status.

```bash
curl http://localhost:8000/api/v1/health
```

Public:

```text
https://iris-ml-api-ms1j.onrender.com/api/v1/health
```

Example response:

```json
{"status":"ok","model_loaded":true}
```

### POST `/api/v1/predict`

Requires `X-API-Key`.

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

PowerShell public test:

```powershell
$body = '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
Invoke-RestMethod -Uri "https://iris-ml-api-ms1j.onrender.com/api/v1/predict" -Method Post -Headers @{"X-API-Key"="YOUR_RENDER_API_KEY"} -ContentType "application/json" -Body $body
```

Example response:

```json
{"prediction":"setosa","confidence":0.9815737196632449,"model_version":"1.0","request_id":"..."}
```

### POST `/api/v1/predict-batch`

Requires `X-API-Key`. Maximum batch size is 100.

```bash
curl -X POST http://localhost:8000/api/v1/predict-batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{"inputs":[{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2},{"sepal_length":6.2,"sepal_width":3.4,"petal_length":5.4,"petal_width":2.3}]}'
```

### GET `/api/v1/model-info`

Requires `X-API-Key`.

```bash
curl http://localhost:8000/api/v1/model-info \
  -H "X-API-Key: your-local-development-key"
```

Example response:

```json
{"model_type":"LogisticRegression","version":"1.0","training_date":"2026-09-01","expected_features":["sepal_length","sepal_width","petal_length","petal_width"]}
```

### POST `/api/v2/predict`

Requires `X-API-Key`. Version 2 returns class probabilities in addition to the predicted class.

```bash
curl -X POST http://localhost:8000/api/v2/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

Example response:

```json
{"prediction":"setosa","probabilities":{"setosa":0.9815737196632449,"versicolor":0.01842626583422591,"virginica":1.4502529259020883e-08},"model_version":"2.0","request_id":"..."}
```

### GET `/metrics`

Prometheus metrics endpoint.

```bash
curl http://localhost:8000/metrics
```

Public:

```text
https://iris-ml-api-ms1j.onrender.com/metrics
```

Look for:

```text
iris_predictions_total
```

## API Documentation

Swagger UI:

```text
Local:  http://localhost:8000/docs
Public: https://iris-ml-api-ms1j.onrender.com/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

## Validation and Security

Prediction fields are required numeric values greater than `0` and at most `10`. Extra fields are rejected.

Protected endpoints require:

```text
X-API-Key: <API_KEY>
```

Missing or incorrect API keys return HTTP `401`. Invalid request bodies return HTTP `422`.

The application reads configuration from environment variables using `pydantic-settings`. The API key must not be committed to Git.

## Environment Variables

Create `.env` from `.env.example`:

```env
API_KEY=your-local-development-key
MODEL_PATH=ml/saved_model/model.joblib
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=Iris ML API
```

`.env` is ignored by Git. For Render, configure `API_KEY` through Render environment variables.

## Project Structure

```text
iris-ml-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── metrics.py
│   ├── security.py
│   ├── models/
│   │   └── schemas.py
│   └── routers/
│       ├── v1.py
│       └── v2.py
├── ml/
│   └── saved_model/
│       ├── model.joblib
│       └── model_metadata.json
├── tests/
│   ├── conftest.py
│   ├── test_batch.py
│   ├── test_health.py
│   ├── test_model_info.py
│   ├── test_predict.py
│   ├── test_security.py
│   └── test_v2.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Local Setup

### Prerequisites

- Docker Desktop
- Docker Compose
- Git

### Clone

```bash
git clone https://github.com/hariharan970/iris-ml-api.git
cd iris-ml-api
```

### Create environment file

PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set a local API key.

### Start with Docker Compose

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

### Stop the service

```bash
docker compose down
```

## Testing

Run the full pytest suite:

```bash
pytest -q
```

Final local test result:

```text
13 passed, 1 warning
```

The test suite covers health checks, predictions, validation, batch requests, model metadata, API-key security, and v2 responses.

GitHub Actions also runs the test suite automatically on pushes to `main` and pull requests targeting `main`.

## Task 19 Integration and Load Testing

Successful local load-test results included:

### 50 Requests

```text
Successful requests: 50
Failed requests: 0
Total test time: 0.291 seconds
Average response: 0.217 seconds
Max response: 0.263 seconds
Min response: 0.155 seconds
```

### 200 Requests

```text
Successful requests: 200
Failed requests: 0
Total test time: 1.536 seconds
Average response: 1.059 seconds
Max response: 1.303 seconds
Min response: 0.560 seconds
```

These are local test observations and are not a cloud performance guarantee.

## Deployment on Render

The API is deployed as a Docker Web Service on Render.

### Public URL

```text
https://iris-ml-api-ms1j.onrender.com
```

### Verified Public Endpoints

```text
https://iris-ml-api-ms1j.onrender.com/api/v1/health
https://iris-ml-api-ms1j.onrender.com/api/v1/predict
https://iris-ml-api-ms1j.onrender.com/api/v2/predict
https://iris-ml-api-ms1j.onrender.com/api/v1/model-info
https://iris-ml-api-ms1j.onrender.com/metrics
https://iris-ml-api-ms1j.onrender.com/docs
```

The deployed service successfully loaded the persisted Logistic Regression model, accepted authenticated predictions, returned v1 and v2 responses, exposed model metadata, and served Prometheus metrics.

### Render Configuration

```text
Repository: hariharan970/iris-ml-api
Branch: main
Runtime: Docker
```

The API key is configured as a Render environment variable and is not stored in the Git repository.

## Independent Extension

### GitHub Actions Automated Testing

The independently chosen extension is **GitHub Actions CI**.

Workflow:

```text
.github/workflows/tests.yml
```

It runs automatically on:

- Pushes to `main`
- Pull requests targeting `main`

The workflow checks out the repository, sets up Python 3.11, installs dependencies, and runs `pytest -q`.

## What I Learned

This project helped me understand how the different parts of a machine-learning service work together.

The main concepts I learned include:

- How to train and persist a scikit-learn machine-learning model.
- How to load a persisted model during FastAPI application startup.
- How Pydantic validation protects an API from invalid input.
- How API versioning allows response contracts to evolve.
- How batch prediction endpoints process multiple inputs.
- How environment-based configuration separates deployment settings and secrets from source code.
- How API-key authentication provides a basic layer of endpoint protection.
- How request IDs and structured logging help with debugging and request tracing.
- How Docker packages the application and its dependencies.
- How Docker Compose makes the application reproducible locally.
- How Prometheus metrics provide operational information about the API.
- How integration and load testing provide evidence that the service works under multiple requests.
- How GitHub Actions can automatically run tests after code changes.
- How to deploy a Dockerized FastAPI machine-learning application to a cloud platform.

## Completion Checklist

- [x] FastAPI service implemented
- [x] Model persisted with joblib
- [x] Input validation
- [x] API versioning
- [x] Batch prediction
- [x] Configuration management
- [x] Structured logging and request IDs
- [x] API-key security
- [x] Prometheus metrics
- [x] Dockerfile
- [x] Docker Compose
- [x] Automated pytest suite
- [x] Task 19 integration/load testing
- [x] GitHub Actions independent extension
- [x] Complete README
- [x] Public Render deployment
- [x] Public Render URL verified end-to-end

## Repository

https://github.com/hariharan970/iris-ml-api

## Public API

https://iris-ml-api-ms1j.onrender.com
