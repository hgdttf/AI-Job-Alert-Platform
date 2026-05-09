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

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

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

    # =========================
    # SEND FIRST EMAIL
    # =========================

    categories = [
        c.strip()
        for c in new_user.categories.split(",")
    ]

    jobs = get_jobs_for_categories(categories)

    print(f"Initial jobs fetched: {len(jobs)}")

    if jobs and len(jobs) > 0:

        send_job_email(
            new_user.email,
            jobs
        )

        new_user.first_email_sent = True

        new_user.last_email_sent_date = (
            datetime.now().strftime("%Y-%m-%d")
        )

        db.commit()

        print(
            f"Initial email sent to "
            f"{new_user.email}"
        )

    return {
        "message": "User registered successfully"
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