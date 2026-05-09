from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

import os


# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()


# =========================
# DATABASE URL
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:

    raise Exception(
        "DATABASE_URL environment variable not found"
    )


# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True
)


# =========================
# SESSION FACTORY
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================
# BASE MODEL
# =========================

Base = declarative_base()


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()