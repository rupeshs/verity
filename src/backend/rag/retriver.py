from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger


class VectorStoreRetriever:
    def __init__(self, embeddings: HuggingFaceEmbeddings):
        self.vector_store = InMemoryVectorStore(embeddings)
        self.embeddings = embeddings

    def ingest_documents(self, documents):
        ids = self.vector_store.add_documents(documents)
        logger.info(f"Indexing completed | chunks: {len(ids)}")

    def get_retriever(self, search_type="mmr", k=4, fetch_k=20, lambda_mult=0.6):
        retriever = self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": lambda_mult,
            },
        )
        return retriever
