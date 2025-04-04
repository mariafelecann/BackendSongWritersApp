from flask import current_app, json

from preprocessing.clean_words_step import CleanTextStep
from preprocessing.lyrics_preprocessing_pipeline import LyricsPreprocessingPipeline
from preprocessing.repetition_score_step import ComputeRepetitionScoreStep
from preprocessing.word_count_step import ComputeWordCountStep


class PredictFacade:
    def __init__(self, model):
        self.model = model
        self.PreprocessingPipeline = LyricsPreprocessingPipeline()
        self.current_preprocessed_lyrics_dataframe = None

    def predict(self, lyrics):
        try:
            try:
                pipeline = (((self.PreprocessingPipeline
                            .add_step(ComputeWordCountStep()))
                            .add_step(CleanTextStep()))
                            .add_step(ComputeRepetitionScoreStep()))

                self.current_preprocessed_lyrics_dataframe = pipeline.run(lyrics)
                print(type(self.current_preprocessed_lyrics_dataframe))
                current_app.logger.info("Finished preprocessing the lyrics")
            except Exception as e:
                current_app.logger.error("Error while preprocessing the lyrics: " + str(e))
                return None

            prediction = self.model.predict(self.current_preprocessed_lyrics_dataframe)
            prediction_list = prediction.tolist()
            result = {"prediction": prediction_list}
            current_app.logger.info("Finished predicting the song's genre: " + str(prediction))
            decision_values = self.model.decision_function(self.current_preprocessed_lyrics_dataframe)
            print(decision_values)
            result["decision_function"] = decision_values.tolist()

            return json.dumps(result)
        except Exception as e:
            current_app.logger.error("Error while predicting the song's genre: " + str(e))
            return None
