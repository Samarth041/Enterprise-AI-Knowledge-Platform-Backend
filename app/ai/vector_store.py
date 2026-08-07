from functools import lru_cache

from langchain_chroma import Chroma

from app.ai.embeddings import get_embeddings
from app.core.config import settings


@lru_cache
def get_vector_store()->Chroma:
    """
    Returm a singleton Chroma vector store
    """

    return Chroma(
        collection_name="enterprise_ai_documents",
        embedding_function=get_embeddings(),
        persist_directory=settings.CHROMA_DB_PATH
    )