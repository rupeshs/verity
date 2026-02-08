import ollama

from backend.llm.abstract_llm import AbstractLLM
from backend.llm.question_generator import QuestionGeneratorMixin
from backend.llm.prompt import get_prompt


class OllamaLLM(AbstractLLM, QuestionGeneratorMixin):
    def __init__(self, model: str):
        self.model = model

    def get_answer_stream(self, context: str, question: str) -> any:
        prompt = get_prompt(context, question)
        stream = self.generate_stream(prompt)
        return stream

    def get_model(self) -> str:
        return self.model

    def generate_stream(self, prompt: str):
        stream = ollama.chat(
            model=self.model,
            stream=True,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.0,
                "think": False,
            },
        )
        return stream
