from unittest.mock import patch
from flask import  json

def test_predict_success(client):

    with patch("services.prediction_service") as mock_service:
        mock_service.predict.return_value = json.dumps({
            "prediction": ["Pop"],
            "class_labels": ["Pop", "Rock"],
            "sentiment": {"label": "Positive 😊", "confidence": 0.95},
            "decision_function": [0.75]
        })

        response = client.post("/ai/predict", json={"lyrics": "some lyrics here"})
        assert response.status_code == 200
        data = response.get_json()
        assert "genre" in data or "prediction" in data or "sentiment" in data

def test_predict_no_lyrics(client):
    response = client.post("/ai/predict", json={})

    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data

def test_predict_exception(client):
    with patch("routes.prediction_routes.prediction_service.predict") as mock_service:
        mock_service.predict.side_effect = Exception("Model failure")

        response = client.post("/ai/predict", json={"lyrics": "some lyrics"})
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
