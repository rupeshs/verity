from abc import ABC, abstractmethod


class AbstractLLM(ABC):
    @abstractmethod
    def generate_stream(self, prompt: str):
        pass

    @abstractmethod
    def get_answer_stream(self, context: str, question: str) -> str:
        pass

    @abstractmethod
    def get_model(self) -> str:
        pass
