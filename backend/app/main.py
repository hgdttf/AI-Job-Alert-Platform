from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .database import Base
from .database import engine

from .routes import router


# =========================
# CREATE DATABASE TABLES
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# FASTAPI APP
# =========================

app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-job-alert-platform.vercel.app",
        "https://jobpulse.xyz",
        "https://www.jobpulse.xyz",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================

app.include_router(router)


# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "message": "JobPulse AI Backend Running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }