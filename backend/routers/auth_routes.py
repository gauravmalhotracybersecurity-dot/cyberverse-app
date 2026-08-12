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
from email_service import send_password_reset_email, send_welcome_email, send_verification_email
from rate_limit import limiter
from config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup")
@limiter.limit(settings.rate_limit_auth)
def signup(request: Request, payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    import uuid as _uuid
    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        is_verified=False,
        verify_nonce=_uuid.uuid4().hex,
        referral_code=_uuid.uuid4().hex[:8],
    )
    if payload.referral_code:
        referrer = db.query(models.User).filter(models.User.referral_code == payload.referral_code).first()
        if referrer:
            user.referred_by_id = referrer.id
            user.bonus_interviews = (user.bonus_interviews or 0) + 1
            user.bonus_resumes = (user.bonus_resumes or 0) + 1
            referrer.bonus_interviews = (referrer.bonus_interviews or 0) + 1
            referrer.bonus_resumes = (referrer.bonus_resumes or 0) + 1
    db.add(user)
    db.commit()
    db.refresh(user)

    link = f"{settings.app_base_url}/app.html?verify={user.id}.{user.verify_nonce}"
    send_verification_email(user.email, link)
    return {"message": "Account created! Check your inbox to verify your email, then log in."}


@router.post("/login", response_model=schemas.TokenResponse)
@limiter.limit(settings.rate_limit_auth)
def login(request: Request, payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first. Check your inbox for the verification link.")
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

    import uuid as _uuid
    nonce = _uuid.uuid4().hex
    user.reset_nonce = nonce
    db.commit()
    reset_token = create_password_reset_token(user.id, nonce)
    send_password_reset_email(user.email, reset_token)
    return generic


@router.post("/reset-password", response_model=schemas.MessageResponse)
@limiter.limit(settings.rate_limit_auth)
def reset_password(
    request: Request, payload: schemas.ResetPasswordRequest, db: Session = Depends(get_db)
):
    try:
        user_id, nonce = verify_password_reset_token(payload.token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not nonce or user.reset_nonce != nonce:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link.")

    user.hashed_password = hash_password(payload.new_password)
    user.reset_nonce = None
    db.commit()
    return schemas.MessageResponse(message="Password updated. You can now log in.")


@router.post("/verify-email", response_model=schemas.MessageResponse)
@limiter.limit(settings.rate_limit_auth)
def verify_email(request: Request, payload: schemas.VerifyEmailRequest, db: Session = Depends(get_db)):
    try:
        uid_str, nonce = payload.token.split(".", 1)
        uid = int(uid_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid verification link.")
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user or not user.verify_nonce or user.verify_nonce != nonce:
        raise HTTPException(status_code=400, detail="Invalid verification link.")
    user.is_verified = True
    user.verify_nonce = None
    db.commit()
    send_welcome_email(user.email, user.full_name or "")
    return schemas.MessageResponse(message="Email verified! You can log in now.")


@router.post("/resend-verification", response_model=schemas.MessageResponse)
@limiter.limit(settings.rate_limit_auth)
def resend_verification(request: Request, payload: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    generic = schemas.MessageResponse(message="If that email is registered and unverified, a new link has been sent.")
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or user.is_verified:
        return generic
    import uuid as _uuid
    user.verify_nonce = _uuid.uuid4().hex
    db.commit()
    link = f"{settings.app_base_url}/app.html?verify={user.id}.{user.verify_nonce}"
    send_verification_email(user.email, link)
    return generic
