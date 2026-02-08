import re
from backend.llm.ollama_llm import AbstractLLM
from backend.search.searxng import search_query
from backend.search.searxng import get_search_results
from loguru import logger


class SearchEngine:
    def __init__(
        self,
        llm: AbstractLLM,
        searxng_base_url: str,
    ):
        self.llm = llm
        self.searxng_base_url = searxng_base_url

    def _generate_questions(self, question: str) -> list[str]:
        response = self.llm.generate_questions(question)
        questions = self._parse_questions(response)
        return questions

    def _parse_questions(self, question: str) -> list[str]:
        return [
            q.strip()
            for q in re.findall(r"^\s*\d+\.\s*(.+)$", question, re.MULTILINE)
            if q.strip()
        ]

    def search(
        self,
        question: str,
        num_results: int = 3,
        extend_questions: bool = True,
    ):
        if extend_questions:
            questions = self._generate_questions(question)
            questions.extend([question])
            logger.info(f"Questions: {questions}")

            return get_search_results(
                questions,
                num_results,
                self.searxng_base_url,
            )
        else:
            return search_query(
                question,
                num_results=num_results,
                searxng_base_url=self.searxng_base_url,
            )
