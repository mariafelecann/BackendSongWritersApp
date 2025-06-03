from flask import current_app, json
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from preprocessing.clean_words_step import CleanTextStep
from preprocessing.lyrics_preprocessing_pipeline import LyricsPreprocessingPipeline
from preprocessing.repetition_score_step import ComputeRepetitionScoreStep
from preprocessing.word_count_step import ComputeWordCountStep
from sentiment_analysis.roEmoLex_utilis import *

class PredictFacade:
    def __init__(self, model):
        self.model = model
        self.PreprocessingPipeline = LyricsPreprocessingPipeline()
        self.current_preprocessed_lyrics_dataframe = None
        # self.sentiment_tokenizer = AutoTokenizer.from_pretrained("DGurgurov/xlm-r_romanian_sentiment")
        # self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("DGurgurov/xlm-r_romanian_sentiment")
        # self.sentiment_pipeline = pipeline("sentiment-analysis", model=self.sentiment_model, tokenizer=self.sentiment_tokenizer)
        roemolex_1 = 'C:\\Users\\maria\\PycharmProjects\\BackendSongWritersApp\\RoEmoLex.csv'
        roemolex_2 = 'C:\\Users\\maria\\PycharmProjects\\BackendSongWritersApp\\RoEmoLex_pos.csv'
        self.lexicon_cuvinte, self.lexicon_expresii = load_roemolex_dual(roemolex_1, roemolex_2)

        if not self.lexicon_cuvinte:
            raise ValueError("Nu s-au putut încărca lexiconurile RoEmoLex.")

    # def analyze_sentiment(self, lyrics):
    #     # Tokenize and truncate to the first 512 tokens
    #     inputs = self.sentiment_tokenizer(
    #         lyrics,
    #         return_tensors="pt",
    #         max_length=512,
    #         truncation=True
    #     )
    #
    #     outputs = self.sentiment_model(**inputs)
    #     probs = outputs.logits.softmax(dim=1)
    #     predicted_class = probs.argmax().item()
    #     confidence = probs.max().item()
    #     label = self.sentiment_model.config.id2label[predicted_class]
    #     label_map = {
    #         "LABEL_0": "Negative 😠",
    #         "LABEL_1": "Neutral 😐",
    #         "LABEL_2": "Positive 😊"
    #     }
    #
    #     sentiment_result = {
    #         "label": label_map.get(label, label),
    #         "confidence": round(confidence, 2)
    #     }
    #
    #     print(sentiment_result)
    #     return sentiment_result

    def analyze_sentiment(self, lyrics):
        rezultat = analizeaza_sentiment_melodie(
            lyrics,
            lexicon_cuvinte=self.lexicon_cuvinte,
            lexicon_expresii=self.lexicon_expresii
        )

        polaritate = rezultat['scor_polaritate']
        if polaritate > 0.2:
            label = "Pozitiv 😊"
        elif polaritate < -0.2:
            label = "Negativ 😠"
        else:
            label = "Neutru 😐"

        sentiment_result = {
            "label": label,
            "confidence": round(abs(polaritate), 2),
            "scor_brut": rezultat['scor_brut'],
            "cuvinte_pozitive": rezultat['cuvinte_pozitive'],
            "cuvinte_negative": rezultat['cuvinte_negative'],
            "nr_cuvinte_semnificative": rezultat['nr_cuvinte_semnificative']
        }

        return sentiment_result


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
            sentiment_result = self.analyze_sentiment(lyrics)
            #print(f"sentiment analysis result: {sentiment_result}")

            prediction = self.model.predict(self.current_preprocessed_lyrics_dataframe)
            class_labels = self.model.named_steps['clf'].classes_.tolist()
            print(class_labels)
            prediction_list = prediction.tolist()
            result = {"prediction": prediction_list,
                      "class_labels": class_labels,
                      "sentiment": sentiment_result
                      }
            current_app.logger.info("Finished predicting the song's genre: " + str(prediction))
            decision_values = self.model.decision_function(self.current_preprocessed_lyrics_dataframe)
            print(decision_values)
            result["decision_function"] = decision_values.tolist()

            return json.dumps(result)
        except Exception as e:
            current_app.logger.error("Error while predicting the song's genre: " + str(e))
            return None
