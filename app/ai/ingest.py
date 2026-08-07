from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.ai.vector_store import get_vector_store

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


def ingest_document(file_path:str):
    loader=PyPDFLoader(file_path)

    documents=loader.load()

    chunks=text_splitter.split_documents(
        documents
    )

    vector_store=get_vector_store()

    vector_store.add_documents(chunks)
    return len(chunks)