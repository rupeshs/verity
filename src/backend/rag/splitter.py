from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def get_splits(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=80, add_start_index=True
    )
    all_splits = text_splitter.split_documents(documents)
    return all_splits
