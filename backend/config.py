import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        ""
    )
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000,https://portfoliosabakhalid.vercel.app"
    )
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")

    class Config:
        # Completely disable .env loading if running on Vercel to avoid file locks
        if os.getenv("VERCEL"):
            env_file = None
        else:
            env_file = ".env" if os.path.exists(".env") else None
        extra = "ignore"

settings = Settings()
