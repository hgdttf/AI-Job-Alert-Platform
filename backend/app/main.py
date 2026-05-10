from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from datetime import datetime
from datetime import timedelta

import pytz

from .database import SessionLocal
from .database import engine
from .database import Base

from .models import User

from .schemas import UserCreate

from .pipeline import get_jobs_for_categories

from .email_service import send_job_email


# =========================================
# DATABASE TABLES
# =========================================

Base.metadata.create_all(bind=engine)


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-job-alert-platform.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# IST TIMEZONE
# =========================================

IST = pytz.timezone("Asia/Kolkata")


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
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "JobPulse API Running"
    }


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health():

    ist_now = datetime.now(IST)

    return {
        "status": "healthy",
        "current_time_ist": ist_now.strftime(
            "%I:%M:%S %p"
        )
    }


# =========================================
# REGISTER USER
# =========================================

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:

            existing_user.categories = ",".join(
                user.categories
            )

            existing_user.delivery_time = (
                user.delivery_time
            )

            db.commit()

            db.refresh(existing_user)

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

        # =========================================
        # IMMEDIATE WELCOME EMAIL
        # =========================================

        try:

            jobs = get_jobs_for_categories(
                user.categories
            )

            if jobs and len(jobs) > 0:

                send_job_email(
                    receiver_email=user.email,
                    jobs=jobs
                )

                print(
                    f"Immediate email sent to "
                    f"{user.email}"
                )

        except Exception as email_error:

            print(
                "Immediate email failed:",
                str(email_error)
            )

        return {
            "message": "Registration successful"
        }

    except Exception as e:

        db.rollback()

        print(
            "REGISTER ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# GET USERS
# =========================================

@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


# =========================================
# RUN SCHEDULER
# =========================================

@app.get("/run-scheduler")
def run_scheduler(
    db: Session = Depends(get_db)
):

    try:

        ist_now = datetime.now(IST)

        today_date = ist_now.date()

        users = db.query(User).all()

        processed_users = 0

        print(
            f"Scheduler running at "
            f"{ist_now.strftime('%I:%M:%S %p')}"
        )

        for user in users:

            try:

                # =================================
                # PREVENT DUPLICATE EMAILS
                # =================================

                if (
                    user.last_email_sent_date
                    == today_date
                ):

                    continue

                # =================================
                # SAFE TIME PARSING
                # =================================

                try:

                    user_time = datetime.strptime(
                        user.delivery_time.strip(),
                        "%I:%M %p"
                    ).time()

                except Exception:

                    print(
                        f"Invalid delivery time "
                        f"for user {user.email}"
                    )

                    continue

                # =================================
                # FLEXIBLE TIME MATCH
                # =================================

                current_minutes = (
                    ist_now.hour * 60
                    + ist_now.minute
                )

                user_minutes = (
                    user_time.hour * 60
                    + user_time.minute
                )

                difference = abs(
                    current_minutes
                    - user_minutes
                )

                # Allow 1 minute tolerance

                if difference > 1:

                    continue

                # =================================
                # CATEGORY PROCESSING
                # =================================

                category_list = [
                    c.strip()
                    for c in user.categories.split(",")
                    if c.strip()
                ]

                jobs = get_jobs_for_categories(
                    category_list
                )

                # =================================
                # SEND EMAIL
                # =================================

                if jobs and len(jobs) > 0:

                    email_sent = send_job_email(
                        receiver_email=user.email,
                        jobs=jobs
                    )

                    if email_sent:

                        user.first_email_sent = True

                        user.last_email_sent_date = (
                            today_date
                        )

                        db.commit()

                        processed_users += 1

                        print(
                            f"Scheduled email sent to "
                            f"{user.email}"
                        )

                    else:

                        print(
                            f"Failed sending email to "
                            f"{user.email}"
                        )

                else:

                    print(
                        f"No jobs found for "
                        f"{user.email}"
                    )

            except Exception as user_error:

                print(
                    "USER PROCESS ERROR:",
                    str(user_error)
                )

                continue

        return {
            "message": "Scheduled check completed",
            "processed_users": processed_users,
            "current_time_ist": ist_now.strftime(
                "%I:%M:%S %p"
            )
        }

    except Exception as e:

        print(
            "SCHEDULER ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )