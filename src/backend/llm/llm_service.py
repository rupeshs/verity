import re

from backend.llm.abstract_llm import AbstractLLM
from backend.llm.prompt import get_prompt, get_question_generator_prompt


class LLMService:
    def __init__(self, llm: AbstractLLM):
        self.llm = llm

    def get_answer_stream(self, context: str, question) -> any:
        prompt = get_prompt(context, question)
        stream = self.llm.generate_stream(prompt)
        return stream

    def generate_questions(
        self,
        question: str,
    ) -> list[str]:
        prompt = get_question_generator_prompt(question)
        stream = self.llm.generate_stream(prompt)

        parts = []
        for chunk in stream:
            parts.append(chunk["message"]["content"])

        return self._parse_questions("".join(parts))

    def _parse_questions(self, question: str) -> list[str]:
        return [
            q.strip()
            for q in re.findall(r"^\s*\d+\.\s*(.+)$", question, re.MULTILINE)
            if q.strip()
        ]
