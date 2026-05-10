from datetime import datetime, timezone

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Text

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
        index=True,
        nullable=False
    )

    categories = Column(
        String,
        nullable=False
    )

    delivery_time = Column(
        String,
        nullable=False
    )

    first_email_sent = Column(
        Boolean,
        default=False
    )

    last_email_sent_date = Column(
        Date,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    onboarding_email_sent_at = Column(
        DateTime,
        nullable=True
    )

    last_scheduler_email_sent_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


class EmailLog(Base):

    __tablename__ = "email_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(
        String,
        nullable=False
    )

    email_type = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )