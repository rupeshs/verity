from abc import ABC, abstractmethod


class AbstractLLM(ABC):
    @abstractmethod
    def generate_stream(self, prompt: str):
        pass
