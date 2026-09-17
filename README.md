# Iris ML API

A Dockerized FastAPI REST API for Iris flower classification using a trained scikit-learn Logistic Regression model.

## Project Overview

The service accepts four Iris flower measurements and predicts one of three classes: `setosa`, `versicolor`, or `virginica`.

The project progressed from model training and API validation to versioned endpoints, structured logging, configuration management, automated testing, Docker/Compose, API-key security, Prometheus metrics, and load testing.

## Features

- Logistic Regression model trained on the scikit-learn Iris dataset
- FastAPI REST API with Pydantic validation
- Versioned prediction endpoints (`v1` and `v2`)
- Batch prediction with a configurable maximum batch size
- Model metadata endpoint
- API-key protection using `X-API-Key`
- Request IDs and structured request logging
- Prometheus monitoring at `/metrics`
- Docker and Docker Compose support
- Automated pytest suite
- GitHub Actions CI on pushes to `main` and pull requests

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
2. The request middleware creates a request ID and records timing.
3. Protected endpoints validate the `X-API-Key` header.
4. Pydantic validates the request body and rejects invalid or missing fields with HTTP 422.
5. The selected versioned router converts the measurements to a NumPy array.
6. The startup lifespan loads the persisted Logistic Regression model into application state.
7. The model returns the predicted class and probabilities.
8. The API returns the response as JSON and logs the result.
9. Prometheus instrumentation records HTTP metrics, while the custom `iris_predictions_total` counter tracks successful predictions by class.

## Dataset and Model

The project uses the built-in Iris dataset from scikit-learn.

Inputs:

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

Classes:

- `setosa`
- `versicolor`
- `virginica`

Algorithm: **Logistic Regression**

The trained model is stored at:

```text
ml/saved_model/model.joblib
```

## API Endpoints

### GET `/`

Basic service response.

```bash
curl http://localhost:8000/
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

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### POST `/api/v1/predict`

Requires `X-API-Key`.

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

The response includes the prediction, confidence, model version, and request ID.

### POST `/api/v1/predict-batch`

Requires `X-API-Key`. The request body contains an `inputs` array. The configured maximum is 100 items.

```bash
curl -X POST http://localhost:8000/api/v1/predict-batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{
    "inputs": [
      {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
      },
      {
        "sepal_length": 6.2,
        "sepal_width": 3.4,
        "petal_length": 5.4,
        "petal_width": 2.3
      }
    ]
  }'
```

### GET `/api/v1/model-info`

Requires `X-API-Key` and returns the stored model metadata JSON.

```bash
curl http://localhost:8000/api/v1/model-info \
  -H "X-API-Key: your-local-development-key"
```

### POST `/api/v2/predict`

Requires `X-API-Key`. Version 2 returns class probabilities in addition to the predicted class.

```bash
curl -X POST http://localhost:8000/api/v2/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-local-development-key" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### GET `/metrics`

Prometheus metrics endpoint.

```bash
curl http://localhost:8000/metrics
```

Look for the custom metric:

```text
iris_predictions_total
```

### API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

## Validation and Security

Prediction fields are required numeric values between greater than 0 and at most 10. Extra fields are rejected.

Protected endpoints require:

```text
X-API-Key: <API_KEY>
```

Missing or incorrect keys return HTTP 401.

The application reads configuration from environment variables using `pydantic-settings`. The secret API key must not be committed to Git.

## Environment Variables

Create `.env` from `.env.example`.

```env
API_KEY=your-local-development-key
MODEL_PATH=ml/saved_model/model.joblib
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=Iris ML API
```

`.env` is ignored by Git.

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

### 1. Clone

```bash
git clone https://github.com/hariharan970/iris-ml-api.git
cd iris-ml-api
```

### 2. Create environment file

PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set a local API key.

### 3. Start with Docker Compose

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

### 4. Stop the service

```bash
docker compose down
```

The Compose configuration mounts `ml/saved_model` read-only into the container, so the persisted model can be reused without changing the application image.

## Testing

Run the full pytest suite locally:

```bash
pytest -q
```

The project includes tests for health checks, predictions, validation, batch requests, model metadata, API-key security, and v2 responses.

The repository also includes a GitHub Actions workflow that runs the test suite automatically on pushes to `main` and pull requests targeting `main`.

## Task 19 Integration and Load Testing

Before the final milestone, the API was exercised with valid and invalid prediction requests and load tests using the secured API-key header.

Observed successful local load-test runs from Task 19 included:

- 50 requests: 50 successful, 0 failed
- 200 requests: 200 successful, 0 failed

These figures are local test observations, not a cloud performance guarantee.

## Deployment on Render

This project is designed to deploy from the existing Dockerfile. Render supports Docker web services and can build the image directly from the repository. citeturn803146search0turn803146search1

### Render setup

1. Open the Render dashboard.
2. Create **New → Web Service**.
3. Connect the GitHub repository `hariharan970/iris-ml-api`.
4. Set the runtime/language to **Docker**.
5. Use the repository's root `Dockerfile`.
6. Add the environment variables from `.env.example`, especially a real secret value for `API_KEY`.
7. Deploy the service.

The Dockerfile listens on Render's runtime `PORT` value and falls back to port `8000` for local Docker runs.

After deployment, validate these paths on the generated `https://<service-name>.onrender.com` URL:

```text
/docs
/api/v1/health
/api/v1/predict
/api/v2/predict
/metrics
```

Remember to send the API key header for protected endpoints.

Render's current documentation notes that free web services can spin down after 15 minutes of inactivity, so the first request after idle time may take longer while the service starts again. citeturn803146search4

## Independent Extension

I chose **GitHub Actions automated testing** as the independent extension.

The workflow is:

```text
.github/workflows/tests.yml
```

It runs the existing pytest suite automatically on:

- Pushes to `main`
- Pull requests targeting `main`

This adds a basic CI safety net so regressions can be detected automatically instead of depending only on local test execution.

## What I Learned

I learned how the pieces of a machine-learning service fit together instead of treating the model and API as separate tasks.

The main things I can now explain are:

- how a persisted scikit-learn model is loaded during FastAPI startup and reused for requests;
- how Pydantic validation protects the API from malformed input;
- why API versioning lets response contracts evolve without breaking the older endpoint;
- how Docker packages the application and Docker Compose makes local reproduction simple;
- how environment-based configuration keeps secrets and deployment settings outside source code;
- how request IDs and structured logs make debugging easier;
- how API-key checks provide a basic layer of endpoint protection;
- how Prometheus metrics expose operational information separately from normal API responses;
- how automated tests and load tests give evidence that the service works before deployment;
- and how GitHub Actions can run regression tests automatically after code changes.

## Self-Assessment

### 1. Can I explain the end-to-end request flow without looking at the code?

**Yes, with one area I would still review before an interview:** the exact interaction between FastAPI middleware, dependency-based API-key validation, request routing, and the Prometheus instrumentation.

### 2. Could a new teammate get the project running from the README?

**Yes for the local Docker setup.** The README gives the repository structure, environment setup, Compose command, endpoints, API-key requirement, and test command. Cloud deployment still requires creating the external Render service and entering the secret environment variable in Render.

### 3. What am I least confident explaining in an interview?

The part I would re-read is **Prometheus monitoring and the custom `iris_predictions_total` metric**, especially the difference between application metrics and request logs, and how Prometheus scrapes the `/metrics` endpoint.

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
- [ ] Public Render URL verified end-to-end

## Repository

https://github.com/hariharan970/iris-ml-api
