from abc import ABC, abstractmethod

class PipelineStep(ABC):
    @abstractmethod
    def process(self, data):
        """Each step will transform the data and return it"""
        pass
