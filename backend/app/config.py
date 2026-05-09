from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    RESEND_API_KEY: str

    EMAIL_FROM: str = "JobPulse AI <alerts@jobpulse.xyz>"

    FRONTEND_URL: str = "https://ai-job-alert-platform.vercel.app"

    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"


settings = Settings()