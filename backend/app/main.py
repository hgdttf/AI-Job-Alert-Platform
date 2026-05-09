from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import User
from backend.app.schemas import UserCreate

from backend.app.services.email_service import send_job_email
from backend.app.services.job_service import get_jobs_for_categories

from datetime import date

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------

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

# -----------------------------
# DATABASE
# -----------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def root():
    return {"message": "JobPulse Backend Running"}

# -----------------------------
# HEALTH
# -----------------------------

@app.get("/health")
def health():
    return {"status": "healthy"}

# -----------------------------
# USERS
# -----------------------------

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "categories": user.categories,
            "delivery_time": user.delivery_time,
            "first_email_sent": user.first_email_sent,
            "last_email_sent_date": user.last_email_sent_date,
        }
        for user in users
    ]

# -----------------------------
# REGISTER
# -----------------------------

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    categories_string = ",".join(user.categories)

    # ---------------------------------
    # UPDATE EXISTING USER
    # ---------------------------------

    if existing_user:

        existing_user.categories = categories_string
        existing_user.delivery_time = user.delivery_time

        db.commit()
        db.refresh(existing_user)

        target_user = existing_user

    # ---------------------------------
    # CREATE NEW USER
    # ---------------------------------

    else:

        new_user = User(
            email=user.email,
            categories=categories_string,
            delivery_time=user.delivery_time,
            first_email_sent=False,
            last_email_sent_date=None,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        target_user = new_user

    # ---------------------------------
    # FETCH JOBS
    # ---------------------------------

    try:

        category_list = [
            c.strip()
            for c in target_user.categories.split(",")
            if c.strip()
        ]

        jobs = get_jobs_for_categories(category_list)

        print("JOBS FOUND:", len(jobs))

    except Exception as e:

        print("JOB FETCH ERROR:", str(e))
        jobs = []

    # ---------------------------------
    # SEND EMAIL
    # ---------------------------------

    try:

        if jobs:

            send_job_email(
                receiver_email=target_user.email,
                jobs=jobs
            )

            target_user.first_email_sent = True
            target_user.last_email_sent_date = str(date.today())

            db.commit()

            return {
                "message": "User registered and email sent successfully"
            }

        else:

            return {
                "message": "User registered but no jobs found"
            }

    except Exception as e:

        print("EMAIL SEND ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(e)}"
        )