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
        # Avoid reading .env if it's locked or missing on Vercel
        env_file = ".env" if os.path.exists(".env") else None
        extra = "ignore"

settings = Settings()
