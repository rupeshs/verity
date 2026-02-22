import asyncio
import re

from langchain_core.documents import Document
from loguru import logger

from backend.documents.crawl import crawl_websites

from utils import trim_txt


class WebDocuments:
    def __init__(
        self,
        search_results: list[dict],
        query: str,
    ):
        self.search_results = search_results
        self.urls = [result["url"] for result in search_results]
        self.query = query
        self.docs = []

    def clean_wiki_refs(self, text: str) -> str:
        # Removes [353],[352]
        return re.sub(r"\[\d+\]", "", text)

    def remove_markdown_images(self, text: str) -> str:
        # Removes ![alt](url)
        return re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)

    def _remove_empty_results(self, results: list[dict]):
        cleaned_results = []
        for result in results:
            if result.markdown is not None:
                cleaned_results.append(result)
            else:
                logger.warning(f"Empty result for url : {result.url}")
        return cleaned_results

    async def generate_documents(self):
        self.crawl_results = await crawl_websites(self.urls)
        self.crawl_results = self._remove_empty_results(self.crawl_results)
        self.docs = []

        for idx, result in enumerate(self.crawl_results):
            ref_clean = self.clean_wiki_refs(result.markdown)
            cleaned = self.remove_markdown_images(ref_clean)
            doc = Document(
                page_content=cleaned,
                metadata={
                    "url": result.url,
                    "title": result.metadata.get("title", ""),
                    "source": "crawl4ai",
                    "doc_id": idx + 1,
                },
            )
            self.docs.append(doc)

    def get_documents(self) -> list[Document]:
        return self.docs

    def generate_documents_sync(self):
        try:
            return asyncio.run(self.generate_documents())
        except RuntimeError as e:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.generate_documents())
