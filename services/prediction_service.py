import joblib

from prediction.prediction_facade import PredictFacade


class PredictionService:
    def __init__(self):
        self.model = joblib.load("model.joblib")
        self.facade = PredictFacade(self.model)

    def predict(self, lyrics):

        return self.facade.predict(lyrics)