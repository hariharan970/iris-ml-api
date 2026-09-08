# Iris ML API

Machine Learning REST API for Iris Flower Classification

## Project Overview

This project will build a REST API that uses a machine learning model to classify Iris flowers based on their physical measurements. The main purpose of the project is to learn how to integrate a machine learning model into a Python API and expose its predictions through a REST endpoint.

## Dataset

The project uses the built-in Iris dataset provided by scikit-learn.

The dataset contains four input features:

- Sepal length
- Sepal width
- Petal length
- Petal width

The model will classify each flower into one of three species:

- Setosa
- Versicolor
- Virginica

## Machine Learning Problem

This is a **supervised classification problem**.

The selected machine learning algorithm is **Logistic Regression**.

The goal is to predict the species of an Iris flower from its four measurements.

## API Contract

The /predict endpoint accepts four numerical measurements of an Iris flower: sepal length, sepal width, petal length, and petal width. The API validates that all required values are provided and are valid numbers. After validation, the values are passed to the trained Logistic Regression model, which predicts whether the flower is Setosa, Versicolor, or Virginica. The API then returns the predicted species as a JSON response. Invalid or missing input will result in a validation error rather than a prediction.

### Endpoint

POST /predict

### Example Input


{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
Example Output
{
    "prediction": "setosa"
}
Request Flow
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
Flow Explanation

First, the client sends the four Iris flower measurements to the /predict endpoint. FastAPI receives the request and validates the input. If the input is valid, the measurements are passed to the trained Logistic Regression model. The model predicts the flower species. Finally, the API returns the prediction to the client in JSON format.

Project Scope

The initial version will focus on one prediction endpoint. The main goal is to understand API development, input validation, machine learning model integration, testing, and deployment.

Complex machine learning techniques are intentionally avoided because the main focus of this project is backend and ML API engineering.

Planned Development
Set up the Python environment.
Create the project folder structure.
Load and train the Iris classification model.
Save the trained model.
Build the FastAPI application.
Add request validation.
Implement the /predict endpoint.
Test the API.
Containerize the application.
Deploy the API.
Technology Stack
Python
FastAPI
Scikit-learn
Pydantic
Uvicorn
Git
GitHub
Docker
Docker Compose
Day 1 Goal

The dataset, machine learning problem, API contract, and initial architecture have been defined before implementation begins.

Environment Variables

The application uses environment variables for configuration.

The .env file contains:

MODEL_PATH=ml/saved_model/model.joblib
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=Iris ML API

The .env file should not be committed to GitHub.

Use .env.example as a template for creating the local .env file.

Project Structure
iris-ml-api/
├── app/
├── ml/
│   └── saved_model/
│       └── model.joblib
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
How to Run the Project
Prerequisites

Make sure you have:

Docker Desktop
Docker Compose
Setup

Create the .env file from .env.example.

On Windows PowerShell:

Copy-Item .env.example .env
Start the API

Build the Docker image and start the API:

docker compose up --build

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs
Start Without Rebuilding

If the Docker image has already been built, start the API with:

docker compose up

This starts the existing Docker image without rebuilding it.

Stop the API

Press:

Ctrl + C

Or run:

docker compose down
Docker Compose

Docker Compose is used to manage the API container.

The API can be started with a single command:

docker compose up

To build the image and start the API:

docker compose up --build

Environment variables are loaded from the .env file instead of being hardcoded in the Compose configuration.

ML Model Volume

The ml/saved_model directory is mounted into the Docker container.

This allows the trained model to be replaced without rebuilding the entire Docker image.

./ml/saved_model
        ↓
/app/ml/saved_model

The model directory is mounted as read-only inside the container.

Testing

The API can be tested through the interactive Swagger documentation:

http://localhost:8000/docs

Send a request to the prediction endpoint using valid Iris flower measurements and verify that the API returns the predicted species.

Development Progress
Set up the Python environment.
Create the project folder structure.
Load and train the Iris classification model.
Save the trained model.
Build the FastAPI application.
Add request validation.
Implement the /predict endpoint.
Test the API.
Introduce API versioning.
Add configuration management.
Containerize the API with Docker.
Orchestrate the API using Docker Compose.
Continue improving security and robustness.
Current Status

The Iris ML API has been containerized using Docker and can be started using Docker Compose.

The API uses environment variables for configuration and mounts the ML model directory as a volume so that the model can be replaced without rebuilding the entire Docker image.