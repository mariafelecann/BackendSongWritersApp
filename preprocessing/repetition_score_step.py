from preprocessing.pypeline_step_interface import PipelineStep
from collections import Counter
import pandas as pd
class ComputeRepetitionScoreStep(PipelineStep):
    def process(self, data):
        """Computes how repetitive the lyrics are"""
        words = data["lyrics"].iloc[0].split()
        total_words = len(words)
        word_counts = Counter(words)
        repeated_word_count = sum(count - 1 for count in word_counts.values() if count > 1)
        repetition_score = repeated_word_count / total_words if total_words > 0 else 0
        df = pd.DataFrame({"repetition_score": [repetition_score]})
        return df
