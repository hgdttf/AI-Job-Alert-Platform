from datetime import date
from threading import Thread

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate

from .pipeline import get_jobs_for_categories
from .email_service import send_job_email


router = APIRouter()


# =========================
# DATABASE SESSION
# =========================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================
# BACKGROUND EMAIL TASK
# =========================

def send_initial_email_background(
    email: str,
    categories: list,
    user_id: int
):

    db = SessionLocal()

    try:

        print(f"Fetching jobs for {email}")

        jobs = get_jobs_for_categories(categories)

        print(f"Jobs fetched: {len(jobs)}")

        if jobs and len(jobs) > 0:

            email_sent = send_job_email(
                email,
                jobs
            )

            if email_sent:

                user = db.query(User).filter(
                    User.id == user_id
                ).first()

                if user:

                    user.first_email_sent = True

                    user.last_email_sent_date = date.today()

                    db.commit()

                    print(
                        f"Initial email sent to {email}"
                    )

            else:

                print(
                    f"Email sending failed for {email}"
                )

        else:

            print(f"No jobs found for {email}")

    except Exception as e:

        print(
            f"Background email error: {str(e)}"
        )

    finally:

        db.close()


# =========================
# REGISTER / UPDATE USER
# =========================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        categories_string = ",".join(user.categories)

        # =========================
        # UPDATE EXISTING USER
        # =========================

        if existing_user:

            existing_user.categories = (
                categories_string
            )

            existing_user.delivery_time = (
                user.delivery_time
            )

            db.commit()

            db.refresh(existing_user)

            print(
                f"Updated existing user: "
                f"{existing_user.email}"
            )

            return {
                "message": (
                    "User preferences updated"
                )
            }

        # =========================
        # CREATE NEW USER
        # =========================

        new_user = User(
            email=user.email,
            categories=categories_string,
            delivery_time=user.delivery_time,
            first_email_sent=False,
            last_email_sent_date=None
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        print(
            f"New user registered: "
            f"{new_user.email}"
        )

        # =========================
        # BACKGROUND EMAIL THREAD
        # =========================

        categories_list = [
            c.strip()
            for c in categories_string.split(",")
        ]

        Thread(
            target=send_initial_email_background,
            args=(
                new_user.email,
                categories_list,
                new_user.id
            )
        ).start()

        return {
            "message": (
                "User registered successfully"
            )
        }

    except Exception as e:

        db.rollback()

        print(f"Register route error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )


# =========================
# GET USERS
# =========================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users