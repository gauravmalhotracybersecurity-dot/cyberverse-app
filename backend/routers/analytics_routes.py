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


@router.post("/lead")
def capture_lead(payload: dict, db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    from datetime import datetime as _dt
    try:
        db.execute(_text("CREATE TABLE IF NOT EXISTS leads (email TEXT, created_at TEXT)"))
        db.execute(_text("INSERT INTO leads (email, created_at) VALUES (:e, :t)"),
                   {"e": (payload or {}).get("email", ""), "t": _dt.utcnow().isoformat()})
        db.commit()
    except Exception:
        pass
    return {"ok": True}


@router.get("/leads")
def list_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    try:
        rows = db.execute(_text("SELECT email, created_at FROM leads ORDER BY created_at DESC LIMIT 200")).fetchall()
    except Exception:
        rows = []
    return [{"email": r[0], "created_at": r[1]} for r in rows]



@router.post("/b2b/lead")
def b2b_lead(payload: dict, db: Session = Depends(get_db)):
    import re as _re
    from sqlalchemy import text as _text
    from datetime import datetime as _dt
    p = payload or {}
    if p.get("website"):
        return {"ok": True}  # honeypot triggered - pretend success, save nothing
    name = str(p.get("name", "") or "").strip()[:200]
    email = str(p.get("email", "") or "").strip()[:200]
    company = str(p.get("company", "") or "").strip()[:200]
    if not name or not company or not _re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", email):
        return {"ok": False, "error": "Name, work email and company are required."}
    size = str(p.get("size", "") or "")[:50]
    industry = str(p.get("industry", "") or "")[:100]
    status = str(p.get("status", "") or "")[:100]
    requirement = str(p.get("requirement", "") or "")[:2000]
    timeline = str(p.get("timeline", "") or "")[:50]
    try:
        db.execute(_text("CREATE TABLE IF NOT EXISTS b2b_leads (name TEXT, email TEXT, company TEXT, size TEXT, industry TEXT, status TEXT, requirement TEXT, timeline TEXT, created_at TEXT)"))
        db.execute(_text("INSERT INTO b2b_leads (name,email,company,size,industry,status,requirement,timeline,created_at) VALUES (:n,:e,:c,:s,:i,:t,:r,:tl,:ca)"),
                   {"n": name, "e": email, "c": company, "s": size, "i": industry, "t": status, "r": requirement, "tl": timeline, "ca": _dt.utcnow().isoformat()})
        db.commit()
    except Exception:
        return {"ok": False, "error": "Could not save your request. Please try again."}
    return {"ok": True}


@router.get("/b2b/leads")
def b2b_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    try:
        rows = db.execute(_text("SELECT name,email,company,size,industry,status,requirement,timeline,created_at FROM b2b_leads ORDER BY created_at DESC LIMIT 200")).fetchall()
    except Exception:
        rows = []
    return [{"name": r[0], "email": r[1], "company": r[2], "size": r[3], "industry": r[4], "status": r[5], "requirement": r[6], "timeline": r[7], "created_at": r[8]} for r in rows]
