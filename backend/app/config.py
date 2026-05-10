from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    RESEND_API_KEY: str

    FROM_EMAIL: str

    ADMIN_EMAIL: str

    ADMIN_PASSWORD: str

    ENVIRONMENT: str = "production"

    class Config:

        env_file = ".env"


settings = Settings()