from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "DATABASE_URL=postgresql://postgres:admin123@localhost:5432/elms_db"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()