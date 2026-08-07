from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

@lru_cache
def get_embeddings()->HuggingFaceEmbeddings:
    """
    Load the embedding model only once.
    """

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={
            "device":"cpu"
        },
        encode_kwargs={
            "normalize_embeddings":True
        }
    )