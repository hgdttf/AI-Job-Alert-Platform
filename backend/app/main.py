from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from .database import Base
from .database import engine

from .routes import router

from .scheduler import run_scheduler


# =========================================================
# CREATE TABLES
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="JobPulse API"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "https://ai-job-alert-platform.vercel.app"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message":
        "JobPulse backend running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status":
        "healthy"
    }


# =========================================================
# RUN SCHEDULER
# =========================================================

@app.get("/run-scheduler")
def scheduler_route():

    return run_scheduler()