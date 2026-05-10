from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from .database import SessionLocal

from .models import User

from .schemas import UserCreate

from .instant_email import send_instant_email


router = APIRouter()


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# REGISTER USER
# =========================================================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

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

            existing_user.is_active = True

            db.commit()

            db.refresh(existing_user)

            # =================================
            # SEND UPDATED ONBOARDING EMAIL
            # =================================

            send_instant_email(
                db=db,
                user=existing_user
            )

            return {
                "message":
                "User updated successfully"
            }

        # =====================================
        # CREATE NEW USER
        # =====================================

        new_user = User(
            email=user.email,

            categories=",".join(
                user.categories
            ),

            delivery_time=user.delivery_time,

            is_active=True
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        # =====================================
        # SEND ONBOARDING EMAIL
        # =====================================

        send_instant_email(
            db=db,
            user=new_user
        )

        return {
            "message":
            "User registered successfully"
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET USERS
# =========================================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    try:

        users = db.query(User).all()

        return users

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )