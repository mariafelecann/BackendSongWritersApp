from preprocessing.pypeline_step_interface import PipelineStep
from sklearn.preprocessing import StandardScaler
import pandas as pd
class ComputeWordCountStep(PipelineStep):
    def process(self, data):
        words = data["lyrics"].iloc[0].split()
        word_count = len(words)
        scaler = StandardScaler()
        word_count_normalized = scaler.fit_transform([[word_count]])[0][0]
        df = pd.DataFrame({"word_count_normalized": [word_count_normalized]})
        return df
