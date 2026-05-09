from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

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

    first_email_sent = Column(
        Boolean,
        default=False
    )

    last_email_sent_date = Column(
        Date,
        nullable=True
    )