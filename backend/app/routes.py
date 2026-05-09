from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from .database import SessionLocal
from .email_service import send_job_email
from .models import User
from .pipeline import get_jobs_for_categories
from .schemas import UserCreate


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        existing_user.categories = ",".join(user.categories)
        existing_user.delivery_time = user.delivery_time

        db.commit()

        return {
            "message": "User updated successfully"
        }

    new_user = User(
        email=user.email,
        categories=",".join(user.categories),
        delivery_time=user.delivery_time,
        first_email_sent=False,
        last_email_sent_date=None
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    categories = [
        c.strip()
        for c in new_user.categories.split(",")
    ]

    jobs = get_jobs_for_categories(categories)

    email_sent = send_job_email(
        new_user.email,
        jobs
    )

    if email_sent:

        new_user.first_email_sent = True

        new_user.last_email_sent_date = datetime.now().date()

        db.commit()

    return {
        "message": "User registered successfully",
        "email_sent": email_sent
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users