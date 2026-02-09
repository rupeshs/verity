from openai import OpenAI
from backend.llm.abstract_llm import AbstractLLM


class OpenAICompatibleLLM(AbstractLLM):
    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str,
    ):
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate_stream(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=0.0,
        )
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield {"message": {"content": delta.content}}
