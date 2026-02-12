import json
import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger

from backend.documents.web_documents import WebDocuments
from backend.llm.embeddings import load_embedding
from backend.llm.llm_factory import LLMFactory
from backend.llm.llm_service import LLMService
from backend.rag.rag_engine import RagEngine
from backend.search.search_engine import SearchEngine
from config import (
    API_HOST,
    API_PORT,
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models...")
    embeddings = load_embedding("sentence-transformers/all-MiniLM-L6-v2")
    llm = LLMFactory.create_llm(
        LLM_PROVIDER,
        LLM_MODEL_PATH,
        DEVICE,
        OPENAI_LLM_BASE_URL,
        OPENAI_LLM_API_KEY,
    )
    llm_service = LLMService(llm)
    app.state.rag_engine = RagEngine(
        embeddings_model=embeddings,
        llm_service=llm_service,
    )
    yield
    del app.state.rag_engine


app = FastAPI(lifespan=lifespan)


def get_rag_engine(request: Request):
    return request.app.state.rag_engine


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def answer_streamer(
    query: str,
    return_src_md: bool,
    rag_engine: RagEngine,
):
    yield "event: search\ndata: Searching...\n\n"
    search_engine = SearchEngine(rag_engine.get_llm_service(), SEARXNG_BASE_URL)
    logger.info("Searching...")
    results = search_engine.search(
        query,
        NUM_SEARCH_RESULTS,
        extend_questions=True,
    )
    webdoc = WebDocuments(results)
    yield "event: read\ndata: Reading...\n\n"
    webdoc.generate_documents_sync()
    docs = webdoc.get_documents()
    rag_engine.load_documents(docs)
    yield "event: think\ndata: Thinking...\n\n"
    rag_stream = rag_engine.get_answer_stream(query, return_src_md)

    for chunk in rag_stream:
        payload = {"type": "token", "text": chunk}
        yield f"event: token\ndata: {json.dumps(payload)}\n\n"

    yield "event: done\ndata: end\n\n"


@app.get("/ask")
async def ask(
    question: str = Query(...),
    rag_engine=Depends(get_rag_engine),
    return_src_md: bool = Query(True),
    description="SSE Streaming endpoint to get answers from Verity",
):
    return StreamingResponse(
        answer_streamer(question, return_src_md, rag_engine),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    show_system_info(DEVICE, LLM_PROVIDER)
    uvicorn.run(
        "api_server:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
    )
