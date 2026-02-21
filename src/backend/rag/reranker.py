from sentence_transformers.cross_encoder import CrossEncoder


def get_reranker(model="BAAI/bge-reranker-base"):
    reranker = CrossEncoder(model, device="cpu")
    return reranker
