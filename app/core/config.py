from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str
    debug:bool

    class Config:
        env_file=".env"


settings=Settings()