from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import router
from .admin_routes import router as admin_router
from .scheduler import start_scheduler


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================

app.include_router(router)

app.include_router(admin_router)


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


# =========================
# START SCHEDULER
# =========================

@app.on_event("startup")
def startup_event():

    start_scheduler()