from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = (
        "mssql+pyodbc:///?odbc_connect="
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=portfolio;"
        "Trusted_Connection=yes"
    )
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
