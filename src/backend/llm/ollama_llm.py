import ollama

from backend.llm.abstract_llm import AbstractLLM


class OllamaLLM(AbstractLLM):
    def __init__(self, model: str):
        self.model = model

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
