from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/achievements", tags=["achievements"])

class AchievementCreate(BaseModel):
    type: str  # "certification", "interview", "hired"
    title: str

@router.post("")
def add_achievement(
    payload: AchievementCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    achievement = models.Achievement(
        user_id=user.id,
        type=payload.type,
        title=payload.title
    )
    db.add(achievement)
    
    # Award XP for achievements
    xp_gained = 0
    if payload.type == "hired":
        xp_gained = 100
    elif payload.type == "certification":
        xp_gained = 50
    else:
        xp_gained = 20
        
    user.xp += xp_gained
    db.commit()
    return {"status": "ok", "xp_awarded": xp_gained}

@router.get("")
def get_achievements(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    achievements = db.query(models.Achievement).filter(models.Achievement.user_id == user.id).all()
    return achievements


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    top = (
        db.query(models.User)
        .filter(models.User.is_verified == True)
        .order_by(models.User.xp.desc())
        .limit(10)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "name": u.full_name or u.email.split("@")[0],
            "xp": u.xp,
            "streak": u.streak_days,
            "is_pro": u.is_pro,
        }
        for i, u in enumerate(top)
    ]
