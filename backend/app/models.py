from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    categories = Column(
        String,
        nullable=False
    )

    delivery_time = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    # =====================================
    # TRACKS ONLY ONBOARDING EMAIL
    # =====================================

    onboarding_email_sent_at = Column(
        DateTime,
        nullable=True
    )

    # =====================================
    # TRACKS ONLY DAILY SCHEDULER
    # =====================================

    last_scheduler_email_sent_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )