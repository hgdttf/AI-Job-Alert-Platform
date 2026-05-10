from datetime import datetime

import pytz

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from sqlalchemy.orm import Session

from .database import SessionLocal
from .database import engine

from .models import Base

from .routes import router

from .scheduler import run_scheduler


# =========================================
# CREATE TABLES
# =========================================

Base.metadata.create_all(
    bind=engine
)


# =========================================
# APP
# =========================================

app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://ai-job-alert-platform.vercel.app",
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================
# ROUTES
# =========================================

app.include_router(router)


IST = pytz.timezone(
    "Asia/Kolkata"
)


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message":
        "JobPulse API running"
    }


# =========================================
# HEALTH
# =========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",

        "current_time_ist":
        datetime.now(IST).strftime(
            "%I:%M %p"
        )
    }


# =========================================
# RUN SCHEDULER
# =========================================

@app.get("/run-scheduler")
def run_scheduler_route():

    db: Session = SessionLocal()

    try:

        processed_users = run_scheduler(db)

        return {
            "message":
            "Scheduler completed",

            "processed_users":
            processed_users
        }

    except Exception as e:

        return {
            "message":
            "Scheduler failed",

            "error":
            str(e)
        }

    finally:

        db.close()