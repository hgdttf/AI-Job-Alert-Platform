from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .database import Base
from .database import engine

from .routes import router


# =========================================
# CREATE TABLES
# =========================================

Base.metadata.create_all(bind=engine)


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI()


# =========================================
# CORS CONFIGURATION
# =========================================

origins = [

    "http://localhost:3000",

    "http://localhost:5173",

    "https://ai-job-alert-platform.vercel.app",

    "https://jobpulse.xyz",

    "https://www.jobpulse.xyz"
]


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================
# ROUTES
# =========================================

app.include_router(router)


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "JobPulse AI Backend Running"
    }


# =========================================
# HEALTH
# =========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
