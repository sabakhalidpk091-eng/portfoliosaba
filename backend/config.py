import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://portfolio:q6bcEVLl57qUb812@cluster0.zvhw8ay.mongodb.net/portfolio_db?retryWrites=true&w=majority&appName=Cluster0"
    )
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
