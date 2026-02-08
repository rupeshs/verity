from collections import defaultdict
from pprint import pprint
from langchain_core.documents import Document


def add_chunk_ids(docs: list[Document]) -> list[Document]:
    grouped = defaultdict(list)
    for doc in docs:
        doc_id = doc.metadata.get("doc_id")
        grouped[doc_id].append(doc)
    final_docs = []
    for doc_id, chunks in grouped.items():
        for idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = idx
            final_docs.append(chunk)

    return final_docs


def create_chunk_map(final_chunks: list[Document]):
    chunk_map = {}

    for chunk in final_chunks:
        key = (chunk.metadata["doc_id"], chunk.metadata["chunk_id"])
        chunk_map[key] = chunk

    return chunk_map


def expand_chunks(
    top_chunks: list[Document], chunk_map: dict, window=1
) -> list[Document]:
    expanded = []

    for chunk in top_chunks:
        doc_id = chunk.metadata["doc_id"]
        chunk_id = chunk.metadata["chunk_id"]

        for i in range(chunk_id - window, chunk_id + window + 1):
            if i < 0:
                continue
            adj = chunk_map.get((doc_id, i))
            if adj:
                expanded.append(adj)

    dedup_chunks = deduplicate_chunks(expanded)
    return sort_chunks(dedup_chunks)


def deduplicate_chunks(chunks: list[Document]) -> list[Document]:
    deduped_chunks = {}
    for chunk in chunks:
        key = (chunk.metadata["doc_id"], chunk.metadata["chunk_id"])
        deduped_chunks[key] = chunk
    return list(deduped_chunks.values())


def sort_chunks(chunks: list[Document]) -> list[Document]:
    sorted_chunks = sorted(
        chunks, key=lambda c: (c.metadata["doc_id"], c.metadata["chunk_id"])
    )
    return sorted_chunks
