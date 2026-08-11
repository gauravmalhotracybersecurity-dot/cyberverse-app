from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/me", response_model=schemas.ProfileResponse)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=schemas.ProfileResponse)
def update_my_profile(
    payload: schemas.ProfileUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.post("/streak-freeze")
def streak_freeze(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_pro:
        raise HTTPException(status_code=403, detail="Pro feature only.")
    if user.streak_days == 0:
        raise HTTPException(status_code=400, detail="No streak to protect.")
    user.streak_freeze_used_today = True
    db.commit()
    return {"message": "Streak freeze activated! Your streak is safe for today."}
