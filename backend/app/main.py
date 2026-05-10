from datetime import datetime

import pytz

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from .database import SessionLocal
from .database import engine
from .models import Base

from .routes import router

from .scheduler import run_scheduler


# =========================================
# CREATE DATABASE TABLES
# =========================================

Base.metadata.create_all(
    bind=engine
)


# =========================================
# FASTAPI APP
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
# INCLUDE ROUTES
# =========================================

app.include_router(router)


# =========================================
# IST TIMEZONE
# =========================================

IST = pytz.timezone(
    "Asia/Kolkata"
)


# =========================================
# DATABASE SESSION
# =========================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "JobPulse API running"
    }


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health_check():

    current_time_ist = datetime.now(
        IST
    ).strftime("%I:%M %p")

    return {
        "status": "healthy",
        "current_time_ist": current_time_ist
    }


# =========================================
# MANUAL SCHEDULER ENDPOINT
# =========================================

@app.get("/run-scheduler")
def run_scheduler_endpoint():

    db: Session = SessionLocal()

    try:

        processed_users = run_scheduler(db)

        return {
            "message": (
                "Scheduler check completed"
            ),
            "processed_users": (
                processed_users
            )
        }

    except Exception as e:

        print(
            f"Scheduler endpoint error: "
            f"{str(e)}"
        )

        return {
            "message": "Scheduler failed",
            "error": str(e)
        }

    finally:

        db.close()