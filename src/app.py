import asyncio
import sys

from dotenv import load_dotenv
from loguru import logger

from backend.documents.web_documents import WebDocuments
from backend.documents.url_ranker import UrlRanker
from backend.llm.llm_factory import LLMFactory
from backend.rag.rag_engine import RagEngine
from backend.search.search_engine import SearchEngine
from backend.llm.llm_service import LLMService
from utils import show_system_info


from backend.llm.embeddings import load_embedding
from config import (
    DEVICE,
    LLM_MODEL_PATH,
    LLM_PROVIDER,
    NUM_SEARCH_RESULTS,
    SEARXNG_BASE_URL,
    OPENAI_LLM_API_KEY,
    OPENAI_LLM_BASE_URL,
    TOP_RESULTS,
)

load_dotenv()
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS A}</green> [{level}] {message}",
)


async def async_main():
    try:
        show_system_info(DEVICE, LLM_PROVIDER)
        llm = LLMFactory.create_llm(
            LLM_PROVIDER,
            LLM_MODEL_PATH,
            DEVICE,
            OPENAI_LLM_BASE_URL,
            OPENAI_LLM_API_KEY,
        )
        embeddings = load_embedding("sentence-transformers/all-MiniLM-L6-v2")
        llm_service = LLMService(llm)
        search_engine = SearchEngine(
            llm_service,
            SEARXNG_BASE_URL,
        )
        url_ranker = UrlRanker()
        rag_engine = RagEngine(
            embeddings_model=embeddings,
            llm_service=llm_service,
        )

        while True:
            query = input("Enter your question (or 'exit' to quit): ")
            if query.lower() == "exit":
                break
            logger.info("Searching...")
            results = search_engine.search(
                query,
                NUM_SEARCH_RESULTS,
                extend_questions=True,
            )
            webdoc = WebDocuments(
                results,
                query,
                url_ranker,
            )
            logger.info("Reading...")
            await webdoc.generate_documents()
            docs = webdoc.get_top_documents(top_k=TOP_RESULTS)
            rag_engine.load_documents(docs)
            rag_stream = rag_engine.get_answer_stream(query)
            for chunk in rag_stream:
                print(chunk, end="", flush=True)

            print("\n")
    except Exception as ex:
        logger.error(ex)


asyncio.run(async_main())
