from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate

from .instant_email import (
    send_instant_email
)


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

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

        send_instant_email(
            existing_user,
            db
        )

        return {
            "message": "User updated successfully"
        }

    # =====================================
    # CREATE NEW USER
    # =====================================

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

    # =====================================
    # SEND INSTANT EMAIL
    # =====================================

    send_instant_email(
        new_user,
        db
    )

    return {
        "message": "User registered successfully"
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users