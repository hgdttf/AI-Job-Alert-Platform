from fastapi import FastAPI

from .database import Base
from .database import engine

from .routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "JobPulse API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }