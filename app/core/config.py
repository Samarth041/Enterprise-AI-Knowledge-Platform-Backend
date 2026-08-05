from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    EMBEDDING_MODEL: str
    CHROMA_DB_PATH: str

    LLM_PROVIDER: str
    LLM_MODEL: str

    GOOGLE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()