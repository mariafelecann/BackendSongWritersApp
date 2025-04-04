from preprocessing.pypeline_step_interface import PipelineStep
import re
import spacy
import pandas as pd
class CleanTextStep(PipelineStep):
    def __init__(self, nlp_model="ro_core_news_sm"):
        self.nlp = spacy.load(nlp_model)
        self.stopwords = self.nlp.Defaults.stop_words

    def process(self, data):
        """Removes punctuation, converts text to lowercase, removes stop words and lemmatizes"""
        lyrics = data["lyrics"].iloc[0]
        lyrics = re.sub(r'[^a-zăâîșțA-ZĂÂÎȘȚ \n]', '', lyrics).lower()
        lyrics = re.sub(r"\[.*?\]|\(bis\s*x\d+\)", "", lyrics)
        lyrics = lyrics.replace("\n", " ")
        replacements = ["bis x", "bisx", "bis", "refren", "verse", "intro", "chorus", "versuri", "strofa", "strofă",
                        "punte"]
        for replacement in replacements:
            lyrics = lyrics.replace(replacement, "")

        lyrics_words = [word for word in lyrics.split() if word not in self.stopwords]
        lyrics = " ".join(lyrics_words)

        doc = self.nlp(lyrics)
        lemmatized_tokens = [token.lemma_ for token in doc]
        lyrics = " ".join(lemmatized_tokens)
        df = pd.DataFrame({"lyrics": [lyrics]})
        return df
