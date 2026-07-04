from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

from app.database import get_db
from app.models.db_models import User
from app.auth.auth_handler import create_access_token
from app.auth.auth_bearer import get_current_user, security
from app.services.cache_service import blacklist_token
from app.monitoring.metrics import auth_events_total

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=request.username,
        email=request.email,
        hashed_password=pwd_context.hash(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    auth_events_total.labels(event="register").inc()
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "username": user.username}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    auth_events_total.labels(event="login").inc()
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "username": user.username}


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: dict = Depends(get_current_user)
):
    """Blacklist the current JWT so it is rejected on all future requests."""
    blacklist_token(credentials.credentials, expires_in=86400)
    auth_events_total.labels(event="logout").inc()
    return {"message": "Logged out successfully"}