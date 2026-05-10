from datetime import datetime, date

from zoneinfo import ZoneInfo

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

    current_time_ist = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%I:%M %p")

    return {
        "status": "healthy",
        "current_time_ist": current_time_ist
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

        categories_string = ",".join(user.categories)

        # =====================================
        # UPDATE EXISTING USER
        # =====================================

        if existing_user:

            existing_user.categories = categories_string

            existing_user.delivery_time = user.delivery_time

            db.commit()

            db.refresh(existing_user)

            target_user = existing_user

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

        # =====================================
        # FETCH JOBS
        # =====================================

        try:

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

        except Exception as e:

            print(
                "JOB FETCH ERROR:",
                str(e)
            )

            jobs = []

        # =====================================
        # SEND EMAIL IMMEDIATELY
        # =====================================

        try:

            if jobs and len(jobs) > 0:

                send_job_email(
                    receiver_email=target_user.email,
                    jobs=jobs
                )

                target_user.first_email_sent = True

                target_user.last_email_sent_date = date.today()

                db.commit()

                print(
                    f"Immediate email sent to "
                    f"{target_user.email}"
                )

                return {
                    "success": True,
                    "message": "Alerts activated successfully"
                }

            else:

                return {
                    "success": True,
                    "message": "Registered successfully but no jobs found currently"
                }

        except Exception as e:

            print(
                "EMAIL ERROR:",
                str(e)
            )

            raise HTTPException(
                status_code=500,
                detail=f"Email sending failed: {str(e)}"
            )

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
# SCHEDULED EMAIL CHECK
# =========================================

@app.get("/run-scheduler")
def run_scheduler(
    db: Session = Depends(get_db)
):

    try:

        ist_now = datetime.now(
            ZoneInfo("Asia/Kolkata")
        )

        current_time = ist_now.strftime(
            "%I:%M %p"
        )

        today_date = date.today()

        users = db.query(User).all()

        processed_users = 0

        print(
            f"Scheduler running at "
            f"{current_time}"
        )

        for user in users:

            try:

                # ==========================
                # PREVENT DUPLICATE EMAILS
                # ==========================

                if (
                    user.last_email_sent_date
                    == today_date
                ):

                    continue

                # ==========================
                # TIME CHECK
                # ==========================

                if (
                    user.delivery_time
                    != current_time
                ):

                    continue

                category_list = [
                    c.strip()
                    for c in user.categories.split(",")
                    if c.strip()
                ]

                jobs = get_jobs_for_categories(
                    category_list
                )

                if jobs and len(jobs) > 0:

                    send_job_email(
                        receiver_email=user.email,
                        jobs=jobs
                    )

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

            except Exception as user_error:

                print(
                    f"USER PROCESS ERROR: "
                    f"{str(user_error)}"
                )

                continue

        return {
            "message": "Scheduled check completed",
            "processed_users": processed_users,
            "current_time_ist": current_time
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