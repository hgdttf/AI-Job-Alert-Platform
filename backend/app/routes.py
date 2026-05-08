from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

router = APIRouter()

security = HTTPBearer()


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
# ADMIN LOGIN
# =========================

@router.post("/admin/login")
def admin_login(data: dict):

    email = data.get("email")
    password = data.get("password")

    ADMIN_EMAIL = "admin@jobpulse.ai"
    ADMIN_PASSWORD = "admin123"

    if (
        email == ADMIN_EMAIL
        and
        password == ADMIN_PASSWORD
    ):

        return {
            "access_token": "admin_token"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )


# =========================
# VERIFY TOKEN
# =========================

def verify_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    if token != "admin_token":

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return token


# =========================
# GET USERS
# =========================

@router.get("/admin/users")
def get_users(
    token: str = Depends(verify_admin),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


# =========================
# DELETE USER
# =========================

@router.delete("/admin/delete-user/{user_id}")
def delete_user(
    user_id: int,
    token: str = Depends(verify_admin),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted"
    }