def test_predict_batch_oversized_returns_422(client):
    payload = {
        "inputs": [
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        ]
        * 101
    }

    response = client.post("/api/v1/predict-batch", json=payload)

    assert response.status_code == 422