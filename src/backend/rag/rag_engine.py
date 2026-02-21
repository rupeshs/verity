from pprint import pprint

from langchain_core.documents import Document
from loguru import logger

from backend.llm.llm_service import LLMService
from backend.rag.chunk_processor import (
    add_chunk_ids,
    create_chunk_map,
    deduplicate_chunks,
    expand_chunks,
    sort_chunks,
)
from backend.rag.reranker import get_reranker
from backend.rag.retriver import VectorStoreRetriever
from backend.rag.selector import select_by_score_gap, should_abort_due_to_low_score
from backend.rag.splitter import get_splits
from utils import trim_txt


class RagEngine:
    def __init__(
        self,
        embeddings_model,
        llm_service: LLMService,
    ):
        self.embeddings = embeddings_model
        self.llm_service = llm_service
        self._context = ""
        self.citation_map = {}
        self.reranker = get_reranker()

    def load_documents(self, docs: list[Document]):
        splits = get_splits(docs)
        chunks = add_chunk_ids(splits)
        self.chunk_map = {}
        self.chunk_map = create_chunk_map(chunks)

        vec_store = VectorStoreRetriever(self.embeddings)
        vec_store.ingest_documents(chunks)
        self.retriever = vec_store.get_retriever(
            search_type="mmr",
            k=8,
            fetch_k=20,
            lambda_mult=0.6,
        )

    def citation_map_to_md(citation_map):
        lines = ["\n### Sources"]
        for cid, data in citation_map.items():
            lines.append(f"[{cid}]: [{data['title']}]({data['url']})")
        return "\n".join(lines)

    def _generate_citation_map(self, docs):
        self.citation_map = {}
        next_id = 1
        for doc in docs:
            url = doc.metadata["url"]
            if url not in self.citation_map:
                self.citation_map[url] = {
                    "citation_id": next_id,
                    "title": doc.metadata.get("title"),
                    "url": url,
                }
                next_id += 1
            doc.metadata["citation_id"] = self.citation_map[url]["citation_id"]

    def _get_context(self, docs: list[Document]) -> str:
        context = "\n\n".join(
            f"[{doc.metadata['citation_id']}]:\n"
            f"Title: {doc.metadata['title']}\n"
            f"{doc.page_content}"
            for doc in docs
        )
        return context

    def rerank_chunks(
        self,
        top_chunks: list[Document],
        top_k=4,
    ) -> list[Document]:
        pairs = [(self.question, doc.page_content) for doc in top_chunks]
        scores = self.reranker.predict(pairs)
        reranked = sorted(zip(top_chunks, scores), key=lambda x: x[1], reverse=True)
        top_reranked = select_by_score_gap(reranked)
        return top_reranked

    def get_answer_stream(
        self,
        question: str,
        use_citations_markdown=False,
        return_sources=True,
    ) -> any:
        self.question = question
        logger.info(f"Retrieving relevant chunks...")
        top_chunks = self.retriever.invoke(question)
        logger.info(f"Retrieved top {len(top_chunks)} chunks")
        # expanded_chunks = expand_chunks(top_chunks, self.chunk_map, 1)
        logger.info(f"Reranking chunks...")
        top_reranked = self.rerank_chunks(top_chunks)

        for doc, score in top_reranked:
            logger.info(f"{trim_txt(doc.metadata['url'])} -> {score:.4f}")
        if should_abort_due_to_low_score(top_reranked):
            message = "I couldn’t find reliable information in the available sources to answer this question."
            logger.warning(message)
            yield message
        else:
            reranked_chunks = [doc for doc, score in top_reranked]
            self._generate_citation_map(reranked_chunks)
            self._context = self._get_context(reranked_chunks)
            logger.info(f"Reranking completed | count: {len(reranked_chunks)}")

            # self._dump_context()
            logger.info("🧠 Preparing answer...")
            stream = self.llm_service.get_answer_stream(self._context, question)

            for chunk in stream:
                yield chunk["message"]["content"]

            if return_sources:
                if use_citations_markdown:
                    line = "\n\n#### Sources \n"
                    yield line
                    for _, data in self.citation_map.items():
                        line = f"- [{data['citation_id']}] - [{trim_txt(data['title'])}]({data['url']}) \n"
                        yield line
                else:
                    yield "\n\nSources : \n"
                    for _, data in self.citation_map.items():
                        yield f"[{data['citation_id']}] - {data['url']})\n"

    def get_context(self) -> str:
        return self._context

    def _dump_context(self):
        with open("context.md", "w", encoding="utf-8") as f:
            f.write(self._context)

    def get_llm_service(self):
        return self.llm_service
