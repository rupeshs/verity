import re

from loguru import logger

from backend.llm.llm_service import LLMService
from backend.search.searxng import search_query


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
            return self._get_top_results(questions, num_results)
        else:
            return self._get_top_results([question], num_results)

    def _get_top_results(
        self,
        questions: list[str],
        num_results: int = 3,
    ):
        top_results = []
        for question in questions:
            results = search_query(
                question,
                num_results=10,
                searxng_base_url=self.searxng_base_url,
            )
            top_results.extend(results[:num_results])

        rank_top = sorted(top_results, key=lambda result: result["score"], reverse=True)
        dedup_results = self._remove_duplicates(rank_top)
        return dedup_results[:num_results]

    def _remove_duplicates(self, results: list) -> list:
        unique = {}

        for result in results:
            url = result["url"]
            score = result["score"]

            if url not in unique or score > unique[url]["score"]:
                unique[url] = result

        deduplicated_results = list(unique.values())
        return deduplicated_results
