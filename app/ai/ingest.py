from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.ai.vector_store import get_vector_store

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


def ingest_document(file_path:str,document_id:str,user_id:str):

    """
    Load a Pdf, split it into chunks, attach metadata,and store the chunks in ChromaDb
    """
    loader=PyPDFLoader(file_path)

    documents=loader.load()

    chunks=text_splitter.split_documents(
        documents
    )

    #========================
    #Add metadata
    #=======================

    for chunk in chunks:
        chunk.metadata.update(
            {
                "document_id":document_id,
                "user_id":user_id
            }
        )

    #======================================
    #Store in Chroma
    #=======================================
    vector_store=get_vector_store()
    print("Number of PDF documents:", len(documents))
    print("Number of chunks:", len(chunks))

    if chunks:
        print("First chunk:", chunks[0].page_content[:200])
        print("First chunk metadata:", chunks[0].metadata)
    vector_store.add_documents(chunks)
    return len(chunks)