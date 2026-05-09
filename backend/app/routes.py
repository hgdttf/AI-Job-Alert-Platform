from datetime import datetime

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
# REGISTER USER
# =========================================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        # =====================================
        # UPDATE EXISTING USER
        # =====================================

        if existing_user:

            existing_user.categories = ",".join(
                user.categories
            )

            existing_user.delivery_time = (
                user.delivery_time
            )

            db.commit()

            db.refresh(existing_user)

            target_user = existing_user

            message = "User updated successfully"

        # =====================================
        # CREATE NEW USER
        # =====================================

        else:

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

            target_user = new_user

            message = "User registered successfully"

        # =====================================
        # FETCH JOBS
        # =====================================

        categories = [
            c.strip()
            for c in target_user.categories.split(",")
        ]

        jobs = get_jobs_for_categories(categories)

        print("=================================")
        print("REGISTER EMAIL FLOW")
        print("USER:", target_user.email)
        print("CATEGORIES:", categories)
        print("JOBS FOUND:", len(jobs))
        print("=================================")

        # =====================================
        # SEND EMAIL
        # =====================================

        if jobs and len(jobs) > 0:

            email_result = send_job_email(
                target_user.email,
                jobs
            )

            print("EMAIL RESULT:", email_result)

            target_user.first_email_sent = True

            target_user.last_email_sent_date = (
                datetime.utcnow().date()
            )

            db.commit()

            return {
                "message": message,
                "email_sent": True,
                "jobs_found": len(jobs)
            }

        else:

            return {
                "message": message,
                "email_sent": False,
                "jobs_found": 0,
                "reason": "No jobs found"
            }

    except Exception as e:

        print("REGISTER ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# GET USERS
# =========================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users

