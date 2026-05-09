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


# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================
# REGISTER USER
# =========================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    clean_email = user.email.strip().lower()

    # =========================
    # PREVENT INVALID EMAILS
    # =========================

    if "@gmail.com@gmail.com" in clean_email:

        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    # =========================
    # CHECK EXISTING USER
    # =========================

    existing_user = db.query(User).filter(
        User.email == clean_email
    ).first()

    # =========================
    # UPDATE EXISTING USER
    # =========================

    if existing_user:

        existing_user.categories = ",".join(user.categories)

        existing_user.delivery_time = user.delivery_time

        db.commit()

        return {
            "message": "User updated successfully"
        }

    # =========================
    # CREATE NEW USER
    # =========================

    new_user = User(
        email=clean_email,
        categories=",".join(user.categories),
        delivery_time=user.delivery_time,
        first_email_sent=False,
        last_email_sent_date=None
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    # =========================
    # FETCH JOBS
    # =========================

    categories = [
        c.strip()
        for c in new_user.categories.split(",")
    ]

    jobs = get_jobs_for_categories(categories)

    print(f"Fetched jobs: {len(jobs)}")

    # =========================
    # SEND FIRST EMAIL
    # =========================

    email_sent = False

    if jobs and len(jobs) > 0:

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


# =========================
# GET USERS
# =========================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users