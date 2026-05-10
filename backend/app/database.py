from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


DATABASE_URL = settings.DATABASE_URL


engine = create_engine(
    DATABASE_URL,

    # ==============================
    # CONNECTION STABILITY
    # ==============================

    pool_pre_ping=True,
    pool_recycle=300,

    # ==============================
    # NEON + AZURE SAFETY
    # ==============================

    pool_size=5,
    max_overflow=10,

    # ==============================
    # BETTER DEBUGGING
    # ==============================

    echo=False
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()