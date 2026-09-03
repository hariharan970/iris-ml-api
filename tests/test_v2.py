def test_v1_and_v2_have_different_response_shapes(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    v1_response = client.post("/api/v1/predict", json=payload)
    v2_response = client.post("/api/v2/predict", json=payload)

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    assert set(v1_data.keys()) == {
        "prediction",
        "confidence",
        "model_version",
        "request_id",
    }
    assert v1_data["prediction"] in {"setosa", "versicolor", "virginica"}
    assert 0 <= v1_data["confidence"] <= 1

    assert set(v2_data.keys()) == {
        "prediction",
        "probabilities",
        "model_version",
        "request_id",
    }
    assert v2_data["prediction"] in {"setosa", "versicolor", "virginica"}
    assert set(v2_data["probabilities"].keys()) == {
        "setosa",
        "versicolor",
        "virginica",
    }
    assert abs(sum(v2_data["probabilities"].values()) - 1.0) < 1e-6

    assert set(v1_data.keys()) != set(v2_data.keys())


def test_v2_missing_field_returns_422(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
    }

    response = client.post("/api/v2/predict", json=payload)

    assert response.status_code == 422


def test_v2_invalid_field_returns_422(client):
    payload = {
        "sepal_length": "invalid",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/api/v2/predict", json=payload)

    assert response.status_code == 422
