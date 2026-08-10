from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import models
from auth import get_current_user
from config import settings
from database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.email.lower() not in [e.strip().lower() for e in settings.admin_email.split(",")]:
        raise HTTPException(status_code=403, detail="Admin only.")
    today = date.today()
    total_users = db.query(func.count(models.User.id)).scalar() or 0
    pro_users = db.query(func.count(models.User.id)).filter(models.User.is_pro == True).scalar() or 0
    total_interviews = db.query(func.count(models.InterviewSession.id)).scalar() or 0
    completed = db.query(func.count(models.InterviewSession.id)).filter(models.InterviewSession.status == "completed").scalar() or 0
    total_resumes = db.query(func.count(models.ResumeReview.id)).scalar() or 0
    mentor_msgs = db.query(func.count(models.MentorMessage.id)).scalar() or 0
    active_today = db.query(func.count(models.User.id)).filter(models.User.last_active_date == today.isoformat()).scalar() or 0

    series = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        n = db.query(func.count(models.User.id)).filter(
            models.User.created_at >= d,
            models.User.created_at < d + timedelta(days=1)
        ).scalar() or 0
        series.append({"date": d.isoformat(), "count": n})

    recent = db.query(models.User).order_by(models.User.created_at.desc()).limit(10).all()
    return {
        "total_users": total_users,
        "pro_users": pro_users,
        "pro_conversion": round(100.0 * pro_users / total_users, 1) if total_users else 0.0,
        "total_interviews": total_interviews,
        "completed_interviews": completed,
        "total_resumes": total_resumes,
        "mentor_messages": mentor_msgs,
        "active_today": active_today,
        "signup_series": series,
        "recent_signups": [
            {"email": u.email, "full_name": u.full_name, "is_pro": bool(u.is_pro),
             "created_at": u.created_at.isoformat()[:10] if u.created_at else ""}
            for u in recent
        ],
    }
