from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime, timedelta

import models
from auth import get_current_user
from config import settings
from database import get_db
from rate_limit import limiter

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

class EventIn(BaseModel):
    name: str
    path: str | None = None
    sid: str | None = None

@router.post("/event")
@limiter.limit("120/hour")
def track(request: Request, payload: EventIn, db: Session = Depends(get_db)):
    user_id = None
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        try:
            from jose import jwt
            p = jwt.decode(auth[7:], settings.jwt_secret, algorithms=["HS256"])
            if p.get("purpose") == "access":
                user_id = int(p["sub"])
        except Exception:
            user_id = None
    db.add(models.Event(user_id=user_id, sid=payload.sid, name=payload.name[:60], path=(payload.path or "")[:200]))
    db.commit()
    return {"ok": True}

@router.get("/funnel")
def funnel(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    admins = [a.strip() for a in settings.admin_email.split(",")]
    if user.email not in admins:
        raise HTTPException(status_code=403, detail="Admins only.")
    cutoff = datetime.utcnow() - timedelta(days=30)
    def cnt(name):
        return db.query(func.count(models.Event.id)).filter(models.Event.name == name, models.Event.created_at >= cutoff).scalar() or 0
    visitors = db.query(func.count(func.distinct(models.Event.sid))).filter(models.Event.created_at >= cutoff).scalar() or 0
    return {
        "visitors": visitors, "signups": cnt("signup"), "logins": cnt("login"),
        "resume": cnt("resume_reviewed"), "interview_started": cnt("interview_started"),
        "interview_completed": cnt("interview_completed"), "paywall_shown": cnt("paywall_shown"),
        "payment_clicked": cnt("payment_clicked"), "ctf_solved": cnt("ctf_solved"),
        "share_copied": cnt("share_copied"),
    }
