from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_SERVICE_URL: str
    USER_SERVICE_URL: str
    JOB_SERVICE_URL: str
    COMPANY_SERVICE_URL: str
    APPLICATION_SERVICE_URL: str

    class Config:
        env_file = ".env.docker"


settings = Settings()