from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

from .routes import router
from .admin_routes import router as admin_router
from .cron_routes import router as cron_router


# =========================
# CREATE DATABASE TABLES
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="JobPulse AI"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-job-alert-platform.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================

app.include_router(router)

app.include_router(admin_router)

app.include_router(cron_router)


# =========================
# ROOT ROUTE
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