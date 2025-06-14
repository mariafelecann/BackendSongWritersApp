from flask import Blueprint, request, jsonify

from services.prediction_service import PredictionService

prediction_bp = Blueprint("ai", __name__)
prediction_service = PredictionService()
@prediction_bp.route("/predict", methods=["POST"])
def predict():
    try:

        data = request.get_json()

        lyrics = data.get("lyrics")

        prediction = prediction_service.predict(lyrics)
        if prediction is not None:
            return jsonify({"genre": prediction}), 200
        else:
            return jsonify({"error": "error while predicting the song's genre"}), 500
    except Exception as e:
        return jsonify({"error": "error while predicting the song's genre", "details": str(e)}), 500