from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from .database import SessionLocal

from .models import User

from .schemas import UserCreate


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
# REGISTER OR UPDATE USER
# =========================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    print("\n========== REGISTER ENDPOINT HIT ==========")

    print("Incoming email:", user.email)
    print("Incoming categories:", user.categories)
    print("Incoming delivery time:", user.delivery_time)

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # =========================
    # UPDATE EXISTING USER
    # =========================

    if existing_user:

        print("Existing user found.")

        existing_user.categories = ",".join(
            user.categories
        )

        existing_user.delivery_time = (
            user.delivery_time
        )

        # reset tracking
        existing_user.first_email_sent = False

        existing_user.last_email_sent_date = None

        db.commit()

        db.refresh(existing_user)

        print("User updated successfully.")

        return {
            "message": (
                "User preferences updated successfully"
            )
        }

    # =========================
    # CREATE NEW USER
    # =========================

    print("Creating new user.")

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

    print("New user created successfully.")

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