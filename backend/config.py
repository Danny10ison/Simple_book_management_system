import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Settings:
    PROJECT_TITLE: str = "BookMangementSystem"
    PROJECT_VERSION: str = "0.0.1"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_BOOK_DB: str = os.getenv("POSTGRES_BOOK_DB", "books")
    POSTGRES_USER_DB: str = os.getenv("POSTGRES_USER_DB", "users")
    BOOK_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_BOOK_DB}"
    USER_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_USER_DB}"
    ALGORITHM = "HS256"
    SECRET_KEY: str = os.getenv("SECRET_KEY")


settings = Settings()
