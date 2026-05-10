from datetime import datetime

import pytz

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from .database import SessionLocal

from .models import User

from .schemas import UserCreate

from .pipeline import get_jobs_for_categories

from .email_service import send_job_email


router = APIRouter()

IST = pytz.timezone(
    "Asia/Kolkata"
)


# =========================================
# DATABASE SESSION
# =========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================
# REGISTER / UPDATE USER
# =========================================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # =====================================
    # EXISTING USER UPDATE
    # =====================================

    if existing_user:

        existing_user.categories = ",".join(
            user.categories
        )

        existing_user.delivery_time = (
            user.delivery_time
        )

        existing_user.updated_at = (
            datetime.now(IST)
        )

        db.commit()

        categories = [
            c.strip()
            for c in existing_user.categories.split(",")
        ]

        jobs = get_jobs_for_categories(
            categories
        )

        if jobs:

            email_sent = send_job_email(
                existing_user.email,
                jobs
            )

            if email_sent:

                existing_user.onboarding_email_sent_at = (
                    datetime.now(IST)
                )

                db.commit()

        return {
            "message":
            "User updated successfully"
        }

    # =====================================
    # NEW USER
    # =====================================

    new_user = User(
        email=user.email,

        categories=",".join(
            user.categories
        ),

        delivery_time=user.delivery_time
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    categories = [
        c.strip()
        for c in new_user.categories.split(",")
    ]

    jobs = get_jobs_for_categories(
        categories
    )

    if jobs:

        email_sent = send_job_email(
            new_user.email,
            jobs
        )

        if email_sent:

            new_user.onboarding_email_sent_at = (
                datetime.now(IST)
            )

            db.commit()

    return {
        "message":
        "User registered successfully"
    }


# =========================================
# GET USERS
# =========================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users