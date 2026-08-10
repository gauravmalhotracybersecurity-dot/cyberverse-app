import datetime as dt

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import settings
from database import get_db
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# bcrypt has a hard 72-byte input limit; truncate defensively so long
# passphrases don't 500 the request.
_MAX_PW_BYTES = 72


def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:_MAX_PW_BYTES]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    pw_bytes = plain.encode("utf-8")[:_MAX_PW_BYTES]
    return bcrypt.checkpw(pw_bytes, hashed.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire, "purpose": "access"}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def create_password_reset_token(user_id: int, nonce: str) -> str:
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.reset_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire, "purpose": "password_reset", "nonce": nonce}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_password_reset_token(token: str) -> int:
    """Returns the user id if the token is a valid, unexpired reset token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        raise ValueError("Invalid or expired reset link.")
    if payload.get("purpose") != "password_reset":
        raise ValueError("Invalid or expired reset link.")
    return int(payload["sub"]), payload.get("nonce")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None or payload.get("purpose") != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
