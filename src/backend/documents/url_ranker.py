from typing import List, Tuple

import numpy as np
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from sentence_transformers import SentenceTransformer


class UrlRanker:
    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=80,
        embedding_model="BAAI/bge-small-en-v1.5",
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.embedding_model = SentenceTransformer(embedding_model)

    def rank(
        self,
        question: str,
        documents: List["Document"],
        top_k: int = 3,
    ) -> List[Tuple[str, float]]:
        """
        Rank document URLs based on similarity to the question using embeddings.

        Returns top_k URLs with their max similarity scores.
        """
        all_chunks = []
        chunk_urls = []

        for doc_idx, doc in enumerate(documents):
            url = doc.metadata.get("url", f"unknown_{doc_idx}")

            try:
                chunks = self.text_splitter.split_text(doc.page_content or "")
                if not chunks:
                    logger.info(f"No chunks generated for URL: {url}")
            except Exception as e:
                logger.error(f"Error splitting document {url}: {e}")
                continue

            all_chunks.extend(chunks)
            chunk_urls.extend([url] * len(chunks))

        if not all_chunks:
            logger.warning("No text chunks generated from documents.")
            return []

        q_embedding = self.embedding_model.encode(question, normalize_embeddings=True)
        chunk_embeddings = self.embedding_model.encode(
            all_chunks, normalize_embeddings=True, batch_size=32
        )

        if len(chunk_embeddings) != len(all_chunks):
            logger.warning("Mismatch between chunk embeddings and chunks count.")
            return []

        scores = np.dot(chunk_embeddings, q_embedding)
        url_scores = {}
        for url, score in zip(chunk_urls, scores):
            score = float(score)

            if url not in url_scores:
                url_scores[url] = score
            else:
                url_scores[url] = max(url_scores[url], score)

        if not url_scores:
            logger.warning("No valid scores found for any URL.")
            return []

        ranked_urls = sorted(url_scores.items(), key=lambda x: x[1], reverse=True)

        return ranked_urls[:top_k]
