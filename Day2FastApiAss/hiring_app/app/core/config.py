from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:admin123@localhost/hiringdb"
    SECRET_KEY: str = "supersecretkey"
    
    class Config:
        env_file = ".env"

settings = Settings()