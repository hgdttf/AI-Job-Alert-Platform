from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import router
from .admin_routes import router as admin_router
from .scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobPulse AI")


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
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "message": "JobPulse AI Backend Running"
    }


# =========================
# START SCHEDULER
# =========================

start_scheduler()