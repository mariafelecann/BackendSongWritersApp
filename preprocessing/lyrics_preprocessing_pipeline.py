from preprocessing.pypeline_step_interface import PipelineStep
import pandas as pd
class LyricsPreprocessingPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step: PipelineStep):
        self.steps.append(step)
        return self

    def run(self, lyrics):
        """Executes all steps in order"""
        data_dict = {"lyrics": [lyrics]}
        # data = pd.DataFrame(data = data_dict)
        # for step in self.steps:
        #     data = step.process(data)
        # return data
        data = pd.DataFrame(data=data_dict)
        results = [data]
        repetition_score = None
        word_count_normalized = None

        for step in self.steps:
            result = step.process(data)
            results.append(result)

            if "lyrics" in result.columns:
                data["lyrics"] = result["lyrics"]
            if "repetition_score" in result.columns:
                repetition_score = result["repetition_score"].iloc[0]
            if "word_count_normalized" in result.columns:
                word_count_normalized = result["word_count_normalized"].iloc[0]

        final_data = pd.DataFrame({
            'lyrics': data["lyrics"].iloc[0],
            'repetition_score': [repetition_score],
            'word_count_normalized': [word_count_normalized]
        })

        return final_data

