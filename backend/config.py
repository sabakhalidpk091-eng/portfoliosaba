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
        # Strictly disabled all local file reading to fix Vercel Resource Busy error
        extra = "ignore"

settings = Settings()
