def test_model_info_returns_expected_metadata(client):
    response = client.get("/api/v1/model-info")

    assert response.status_code == 200

    data = response.json()

    assert "model_type" in data
    assert "version" in data
    assert "training_date" in data
    assert "expected_features" in data

    assert data["model_type"] == "LogisticRegression"
    assert len(data["expected_features"]) == 4