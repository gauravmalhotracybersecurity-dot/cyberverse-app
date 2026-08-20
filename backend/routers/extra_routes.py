from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date

import models
from auth import get_current_user
from database import get_db

router = APIRouter(tags=["extra"])

@router.get("/api/leaderboard")
def leaderboard(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.User).order_by(models.User.xp.desc()).limit(10).all()
    users = []
    for u in rows:
        users.append({"name": u.full_name or u.email.split("@")[0], "xp": u.xp or 0,
                      "is_pro": bool(getattr(u, "is_premium", False) or getattr(u, "is_pro", False))})
    return {"users": users}

