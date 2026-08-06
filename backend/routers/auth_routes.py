from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from database import get_db
from email_service import send_password_reset_email
from rate_limit import limiter
from config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.TokenResponse)
@limiter.limit(settings.rate_limit_auth)
def signup(request: Request, payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return schemas.TokenResponse(access_token=token)


@router.post("/login", response_model=schemas.TokenResponse)
@limiter.limit(settings.rate_limit_auth)
def login(request: Request, payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    token = create_access_token(user.id)
    return schemas.TokenResponse(access_token=token)


@router.post("/forgot-password", response_model=schemas.MessageResponse)
@limiter.limit(settings.rate_limit_auth)
def forgot_password(
    request: Request, payload: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)
):
    # Always return the same generic message whether or not the account
    # exists, so this endpoint can't be used to enumerate registered emails.
    generic = schemas.MessageResponse(
        message="If that email is registered, a reset link has been sent."
    )
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        return generic

    reset_token = create_password_reset_token(user.id)
    send_password_reset_email(user.email, reset_token)
    return generic


@router.post("/reset-password", response_model=schemas.MessageResponse)
@limiter.limit(settings.rate_limit_auth)
def reset_password(
    request: Request, payload: schemas.ResetPasswordRequest, db: Session = Depends(get_db)
):
    try:
        user_id = verify_password_reset_token(payload.token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link.")

    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return schemas.MessageResponse(message="Password updated. You can now log in.")
