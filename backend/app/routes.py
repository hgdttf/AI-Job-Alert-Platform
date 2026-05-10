from datetime import date

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from .database import SessionLocal

from .models import User

from .schemas import UserCreate

from .pipeline import get_jobs_for_categories

from .email_service import send_job_email


router = APIRouter()


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

        db.commit()

        categories = [
            c.strip()
            for c in existing_user.categories.split(",")
        ]

        jobs = get_jobs_for_categories(
            categories
        )

        print(
            "Fetched jobs for updated user:",
            len(jobs)
        )

        if jobs:

            email_sent = send_job_email(
                existing_user.email,
                jobs
            )

            if email_sent:

                existing_user.first_email_sent = True

                db.commit()

        return {
            "message": (
                "User updated successfully"
            )
        }

    # =====================================
    # NEW USER REGISTRATION
    # =====================================

    new_user = User(
        email=user.email,

        categories=",".join(
            user.categories
        ),

        delivery_time=user.delivery_time,

        first_email_sent=False,

        # IMPORTANT:
        # Scheduler controls this field ONLY
        last_email_sent_date=None
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

    print(
        "Fetched jobs for new user:",
        len(jobs)
    )

    if jobs:

        email_sent = send_job_email(
            new_user.email,
            jobs
        )

        if email_sent:

            # ONLY TRACK IMMEDIATE EMAIL
            new_user.first_email_sent = True

            db.commit()

    return {
        "message": (
            "User registered successfully"
        )
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