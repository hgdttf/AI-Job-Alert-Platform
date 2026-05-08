from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)

    categories = Column(String, nullable=False)

    delivery_time = Column(String, nullable=False)

    last_sent_date = Column(String, nullable=True)

    initial_email_sent = Column(String, default="false")