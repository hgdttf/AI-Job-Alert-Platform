from datetime import date

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import BackgroundTasks

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
# BACKGROUND EMAIL TASK
# =========================================

def process_and_send_email(user_email, categories):

    try:

        jobs = get_jobs_for_categories(categories)

        print(f"Jobs fetched: {len(jobs)}")

        if jobs and len(jobs) > 0:

            send_job_email(
                receiver_email=user_email,
                jobs=jobs
            )

            print(
                f"Email sent successfully to "
                f"{user_email}"
            )

    except Exception as e:

        print("BACKGROUND EMAIL ERROR:", str(e))


# =========================================
# REGISTER USER
# =========================================

@app.post("/register")
def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

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
    # BACKGROUND EMAIL
    # =====================================

    category_list = [
        c.strip()
        for c in target_user.categories.split(",")
        if c.strip()
    ]

    background_tasks.add_task(
        process_and_send_email,
        target_user.email,
        category_list
    )

    target_user.first_email_sent = True

    target_user.last_email_sent_date = date.today()

    db.commit()

    # =====================================
    # INSTANT RESPONSE
    # =====================================

    return {
        "message": "Alerts activated successfully"
    }