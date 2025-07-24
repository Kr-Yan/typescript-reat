from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str="GMGN Trading API"
    debug: bool=True
    host: str= "0.0.0.0"
    port: int=3001

    allowed_origins: list=["http://localhost:3000"]

    class Config:
        env_file=".env"
settings= Settings()