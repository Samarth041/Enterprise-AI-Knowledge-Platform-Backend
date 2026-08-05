from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

@lru_cache
def get_llm():
    """
    Returns a singleton LLM instance
    """

    return ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )