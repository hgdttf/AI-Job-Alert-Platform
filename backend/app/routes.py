from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate

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

    # Check if user already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        email=user.email,
        categories=",".join(user.categories),
        delivery_time=user.delivery_time
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "categories": new_user.categories,
            "delivery_time": new_user.delivery_time
        }
    }


# =========================
# GET USERS
# =========================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    result = []

    for user in users:

        result.append({
            "id": user.id,
            "email": user.email,
            "categories": user.categories,
            "delivery_time": user.delivery_time
        })

    return result