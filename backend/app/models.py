from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

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
        index=True
    )

    categories = Column(String)

    delivery_time = Column(String)

    # =========================
    # EMAIL TRACKING
    # =========================

    first_email_sent = Column(
        Boolean,
        default=False
    )

    last_email_sent_date = Column(
        String,
        nullable=True
    )