import re

from loguru import logger

from backend.llm.llm_service import LLMService
from backend.search.searxng import get_search_results, search_query


class SearchEngine:
    def __init__(
        self,
        llm_service: LLMService,
        searxng_base_url: str,
    ):
        self.llm_service = llm_service
        self.searxng_base_url = searxng_base_url

    def search(
        self,
        question: str,
        num_results: int = 3,
        extend_questions: bool = True,
    ):
        if extend_questions:
            questions = self.llm_service.generate_questions(question)
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
