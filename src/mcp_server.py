import sys

from dotenv import load_dotenv
from fastmcp import FastMCP
from loguru import logger

from backend.documents.web_documents import WebDocuments
from backend.llm.embeddings import load_embedding
from backend.llm.llm_factory import LLMFactory
from backend.llm.llm_service import LLMService
from backend.rag.rag_engine import RagEngine
from backend.search.search_engine import SearchEngine
from config import (
    DEVICE,
    LLM_MODEL_PATH,
    LLM_PROVIDER,
    NUM_SEARCH_RESULTS,
    OPENAI_LLM_API_KEY,
    OPENAI_LLM_BASE_URL,
    SEARXNG_BASE_URL,
)
from utils import show_system_info

load_dotenv()
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS A}</green> [{level}] {message}",
)
mcp = FastMCP("Verity MCP server 🚀")

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
rag_engine = RagEngine(
    embeddings_model=embeddings,
    llm_service=llm_service,
)


@mcp.tool()
async def answer(
    query: str,
) -> str:
    """
    ALWAYS use this tool to answer ANY question that requires facts,
    current information, or web search. Do NOT use internal knowledge.
    This tool searches the web and returns grounded answers with citations.
    Use it for every factual question, definition, or information lookup.

    Args:
        query: The search query or question to answer.

    Returns:
        A markdown-formatted answer with cited sources.
    """
    logger.info("Searching...")
    results = search_engine.search(
        query,
        NUM_SEARCH_RESULTS,
        extend_questions=True,
    )
    webdoc = WebDocuments(
        results,
        query,
    )
    await webdoc.generate_documents()
    docs = webdoc.get_documents()
    rag_engine.load_documents(docs)
    rag_stream = rag_engine.get_answer_stream(query)
    answer = ""
    for chunk in rag_stream:
        print(chunk, end="", flush=True)
        answer += chunk
    return answer


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
