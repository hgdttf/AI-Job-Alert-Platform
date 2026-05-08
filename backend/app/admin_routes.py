from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

from .schemas import UserCreate

from datetime import datetime


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

        existing_user.categories = ", ".join(
            user.categories
        )

        existing_user.delivery_time = (
            user.delivery_time
        )

        existing_user.last_sent_date = None

        db.commit()

        return {
            "message": "User updated successfully"
        }

    new_user = User(
        email=user.email,
        categories=", ".join(user.categories),
        delivery_time=user.delivery_time,
        created_at=datetime.now(),
        last_sent_date=None
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

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


# =========================
# ADMIN CONFIG
# =========================

ADMIN_EMAIL = "admin@jobpulse.ai"

ADMIN_PASSWORD = "Admin@123"


# =========================
# ADMIN LOGIN
# =========================

@router.post("/admin/login")
def admin_login(data: dict):

    email = data.get("email")

    password = data.get("password")

    if (
        email == ADMIN_EMAIL and
        password == ADMIN_PASSWORD
    ):

        return {
            "access_token": "admin-token"
        }

    return {
        "error": "Invalid credentials"
    }


# =========================
# ADMIN GET USERS
# =========================

@router.get("/admin/users")
def admin_get_users(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):

    if authorization != "Bearer admin-token":

        return []

    users = db.query(User).all()

    return users


# =========================
# ADMIN DELETE USER
# =========================

@router.delete("/admin/delete-user/{user_id}")
def delete_user(
    user_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):

    if authorization != "Bearer admin-token":

        return {
            "error": "Unauthorized"
        }

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "error": "User not found"
        }

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }