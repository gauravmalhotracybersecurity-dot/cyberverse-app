from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/stories", tags=["stories"])

class StoryIn(BaseModel):
    title: str
    source: str = "manual"
    s: str
    t: str = ""
    a: str
    r: str = ""

@router.get("")
def list_stories(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.Story).filter(models.Story.user_id == user.id).order_by(models.Story.id.desc()).all()
    return [{"id": x.id, "title": x.title, "s": x.s, "t": x.t, "a": x.a, "r": x.r} for x in rows]

@router.post("")
def add_story(payload: StoryIn, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if len(payload.s) < 10 or len(payload.a) < 10:
        raise HTTPException(status_code=400, detail="Give Situation and Action a bit more detail (10+ chars each).")
    db.add(models.Story(user_id=user.id, title=payload.title[:120] or "My story", source=payload.source[:40],
                        s=payload.s, t=payload.t, a=payload.a, r=payload.r))
    user.xp = (user.xp or 0) + 5
    db.commit()
    return {"ok": True}
