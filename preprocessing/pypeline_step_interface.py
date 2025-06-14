from abc import ABC, abstractmethod

class PipelineStep(ABC):
    @abstractmethod
    def process(self, data):
        pass
