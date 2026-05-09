from datetime import datetime
from datetime import date

import pytz

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate

from .pipeline import get_jobs_for_categories
from .email_service import send_job_email


# =========================================
# FASTAPI
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
# DATABASE
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
        "message": "JobPulse Backend Running"
    }


# =========================================
# HEALTH
# =========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


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
# REGISTER USER
# =========================================

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        categories_string = ",".join(
            user.categories
        )

        # =====================================
        # UPDATE EXISTING USER
        # =====================================

        if existing_user:

            existing_user.categories = (
                categories_string
            )

            existing_user.delivery_time = (
                user.delivery_time
            )

            db.commit()

            db.refresh(existing_user)

            target_user = existing_user

            print(
                f"Updated existing user: "
                f"{target_user.email}"
            )

        # =====================================
        # CREATE NEW USER
        # =====================================

        else:

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

            target_user = new_user

            print(
                f"Created new user: "
                f"{target_user.email}"
            )

        # =====================================
        # FETCH JOBS
        # =====================================

        category_list = [
            c.strip()
            for c in target_user.categories.split(",")
            if c.strip()
        ]

        jobs = get_jobs_for_categories(
            category_list
        )

        print(
            f"Jobs fetched: {len(jobs)}"
        )

        # =====================================
        # SEND EMAIL
        # =====================================

        if jobs and len(jobs) > 0:

            send_job_email(
                receiver_email=target_user.email,
                jobs=jobs
            )

            target_user.first_email_sent = True

            target_user.last_email_sent_date = (
                date.today()
            )

            db.commit()

            print(
                f"Initial email sent to "
                f"{target_user.email}"
            )

            return {
                "message":
                "User registered successfully and email sent"
            }

        else:

            return {
                "message":
                "User registered but no jobs found"
            }

    except Exception as e:

        print(
            "REGISTER ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# RUN JOB CHECK
# =========================================

@app.get("/run-job-check")
def run_job_check(
    db: Session = Depends(get_db)
):

    try:

        # =====================================
        # INDIA TIMEZONE
        # =====================================

        india_timezone = pytz.timezone(
            "Asia/Kolkata"
        )

        current_time = datetime.now(
            india_timezone
        ).strftime("%I:%M %p")

        print(
            f"Current IST Time: "
            f"{current_time}"
        )

        users = db.query(User).all()

        processed_users = 0

        for user in users:

            print(
                f"Checking {user.email} "
                f"scheduled for "
                f"{user.delivery_time}"
            )

            # =================================
            # MATCH TIME
            # =================================

            if user.delivery_time == current_time:

                categories = [
                    c.strip()
                    for c in user.categories.split(",")
                    if c.strip()
                ]

                jobs = get_jobs_for_categories(
                    categories
                )

                print(
                    f"Jobs for {user.email}: "
                    f"{len(jobs)}"
                )

                if jobs and len(jobs) > 0:

                    send_job_email(
                        receiver_email=user.email,
                        jobs=jobs
                    )

                    user.first_email_sent = True

                    user.last_email_sent_date = (
                        datetime.now(
                            india_timezone
                        ).date()
                    )

                    db.commit()

                    processed_users += 1

                    print(
                        f"Scheduled email sent to "
                        f"{user.email}"
                    )

        return {
            "message":
            "Scheduled check completed",
            "processed_users":
            processed_users,
            "current_time_ist":
            current_time
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