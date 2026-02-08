from langchain_huggingface import HuggingFaceEmbeddings


def load_embedding(
    embedding_model: str,
):
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    return embeddings
