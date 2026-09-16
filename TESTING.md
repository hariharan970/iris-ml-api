# Task 19 — Integration Testing, Load Testing, and Bug Fixing

## 1. Overview

This document records the integration testing, load testing, and bug fixing performed for the Iris ML API.

The API was tested as a fully containerized FastAPI application running through Docker Compose.

---

## 2. Environment

* Framework: FastAPI
* Language: Python
* Machine Learning: scikit-learn
* Containerization: Docker
* Orchestration: Docker Compose
* Testing: pytest
* Load Testing: Python `asyncio` + `httpx`
* Monitoring: Prometheus metrics

---

## 3. Docker Integration Testing

The application was started using:

```bash
docker compose up --build
```

The ML model loaded successfully inside the Docker container.

### Integration endpoints tested

| Endpoint                | Method | Result |
| ----------------------- | ------ | ------ |
| `/api/v1/health`        | GET    | PASS   |
| `/api/v1/predict`       | POST   | PASS   |
| `/api/v1/predict-batch` | POST   | PASS   |
| `/metrics`              | GET    | PASS   |

### Health Check

Request:

```text
GET /api/v1/health
```

Result:

```json
{
    "status": "ok",
    "model_loaded": true
}
```

The API confirmed that the ML model was loaded successfully.

### Single Prediction

Request:

```text
POST /api/v1/predict
```

A valid Iris input was submitted with the required `X-API-Key` header.

Result:

* HTTP 200
* Prediction returned successfully
* Confidence score returned
* Model version returned
* Request ID returned

Example prediction:

```text
prediction: setosa
confidence: 0.9815737196632449
model_version: 1.0
```

### Batch Prediction

Request:

```text
POST /api/v1/predict-batch
```

Multiple valid Iris inputs were submitted.

Result:

* HTTP 200
* Predictions returned successfully
* Confidence values returned
* Request ID returned

Validation tests were also performed for invalid batch sizes.

An empty batch was rejected correctly, and a batch containing more than the configured maximum number of inputs was also rejected correctly.

### Metrics

Request:

```text
GET /metrics
```

Result:

* Prometheus metrics were successfully exposed.
* Prediction counters were recorded.
* HTTP request counters were recorded.
* Request duration metrics were recorded.
* Process resource metrics were available.

---

## 4. Load Testing

A custom asynchronous Python load-testing script using `httpx` was used to send concurrent requests to:

```text
POST /api/v1/predict
```

### 50 Concurrent Requests

| Metric              |        Result |
| ------------------- | ------------: |
| Total requests      |            50 |
| Successful requests |            50 |
| Failed requests     |             0 |
| Total test time     | 0.291 seconds |
| Average response    | 0.217 seconds |
| Maximum response    | 0.263 seconds |
| Minimum response    | 0.155 seconds |

Result:

**50/50 requests completed successfully with zero failures.**

### 200 Concurrent Requests — Initial Test

| Metric              |        Result |
| ------------------- | ------------: |
| Total requests      |           200 |
| Successful requests |           200 |
| Failed requests     |             0 |
| Total test time     | 1.536 seconds |
| Average response    | 1.059 seconds |
| Maximum response    | 1.303 seconds |
| Minimum response    | 0.560 seconds |

Result:

**200/200 requests completed successfully with zero failures.**

### 200 Concurrent Requests — Final Test

After the security fix was applied, the load test was repeated.

| Metric              |        Result |
| ------------------- | ------------: |
| Total requests      |           200 |
| Successful requests |           200 |
| Failed requests     |             0 |
| Total test time     | 1.565 seconds |
| Average response    | 1.115 seconds |
| Maximum response    | 1.375 seconds |
| Minimum response    | 0.533 seconds |

Result:

**200/200 requests completed successfully with zero failures.**

The load test confirmed that the container remained operational under 200 concurrent prediction requests.

---

## 5. Bug Found

### Issue: Missing API Key Protection on V2 Prediction Endpoint

During security validation, the V1 prediction endpoint was protected by the API-key dependency:

```text
/api/v1/predict
```

However, the V2 prediction endpoint:

```text
/api/v2/predict
```

did not use the same API-key verification dependency.

This created an inconsistent security configuration where V1 required authentication but V2 could accept prediction requests without an API key.

---

## 6. Bug Fix

The V2 prediction endpoint was updated to use the existing API-key verification dependency.

The endpoint now requires:

```text
X-API-Key
```

before processing prediction requests.

### Validation

#### Request without API key

Result:

```text
HTTP 401
Invalid or missing API key
```

#### Request with valid API key

Result:

```text
HTTP 200
Prediction successful
```

The V2 endpoint returned:

* Prediction
* Class probabilities
* Model version `2.0`
* Request ID

The security fix was therefore verified successfully.

---

## 7. Final Test Summary

| Test                     | Result                    |
| ------------------------ | ------------------------- |
| Docker build             | PASS                      |
| Docker container startup | PASS                      |
| Health endpoint          | PASS                      |
| V1 prediction            | PASS                      |
| Batch prediction         | PASS                      |
| Prometheus metrics       | PASS                      |
| 50 concurrent requests   | PASS — 50/50              |
| 200 concurrent requests  | PASS — 200/200            |
| V2 without API key       | PASS — correctly rejected |
| V2 with API key          | PASS                      |
| Security bug fixed       | PASS                      |

---

## 8. Conclusion

The Iris ML API was tested end-to-end inside the Dockerized environment.

Integration testing confirmed that the main API endpoints, batch prediction, health check, and Prometheus metrics were functioning correctly.

Load testing with 50 and 200 concurrent requests completed with zero failed requests.

A real security issue was identified in the V2 prediction endpoint, where API-key protection was missing. The endpoint was updated to use the existing API-key verification dependency and was successfully validated with both unauthorized and authorized requests.

Task 19 testing and bug-fixing activities were completed successfully.
