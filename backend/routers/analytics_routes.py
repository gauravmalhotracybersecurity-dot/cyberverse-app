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



# ================= BILLING / SUBSCRIPTIONS (Razorpay-ready) =================
from fastapi import Request as _Request
from fastapi import HTTPException as _HTTPException
from sqlalchemy import text as _btext
from plans import PLANS as _PLANS


@router.get("/plans")
def list_plans():
    return _PLANS


@router.get("/billing/subscription")
def my_subscription(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        row = db.execute(_btext("SELECT plan, status, current_period_end FROM subscriptions WHERE user_id=:u AND status='active' ORDER BY created_at DESC LIMIT 1"), {"u": user.id}).fetchone()
    except Exception:
        row = None
    if row:
        return {"plan": row[0], "status": row[1], "renews": row[2]}
    legacy = "pro" if getattr(user, "is_pro", False) else "free"
    return {"plan": legacy, "status": "active", "renews": None}


@router.post("/billing/checkout")
def billing_checkout(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import os
    plan_key = str((payload or {}).get("plan", ""))
    if plan_key not in _PLANS or plan_key == "free":
        raise _HTTPException(status_code=400, detail="Invalid plan")
    key_id = os.environ.get("RAZORPAY_KEY_ID", "")
    if not key_id:
        return {"status": "coming_soon", "plan": plan_key, "message": "Online payments activate soon - early users are upgraded manually."}
    # TODO(Razorpay): create order with razorpay client (amount = price_inr*100, currency INR),
    # return order_id + key_id for the checkout overlay; activation happens in /billing/webhook.
    return {"status": "coming_soon", "plan": plan_key}


@router.post("/billing/webhook")
async def billing_webhook(request: _Request):
    # TODO(Razorpay): verify X-Razorpay-Signature (HMAC-SHA256 of raw body with RAZORPAY_KEY_SECRET)
    # BEFORE writing the subscription row. Never trust the payload without signature check.
    return {"ok": False, "error": "Payment provider not configured yet"}


@router.post("/billing/activate")
def billing_activate(request: _Request, payload: dict, db: Session = Depends(get_db)):
    import os
    from datetime import datetime as _dt, timedelta as _td
    secret = os.environ.get("ADMIN_SECRET", "")
    if not secret or request.headers.get("x-admin-secret") != secret:
        raise _HTTPException(status_code=403, detail="Forbidden")
    email = str((payload or {}).get("email", ""))
    plan = str((payload or {}).get("plan", "pro"))
    if plan not in _PLANS or plan == "free":
        raise _HTTPException(status_code=400, detail="Invalid plan")
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        raise _HTTPException(status_code=404, detail="User not found")
    db.execute(_btext("CREATE TABLE IF NOT EXISTS subscriptions (user_id INTEGER, plan TEXT, status TEXT, provider TEXT, provider_payment_id TEXT, current_period_end TEXT, created_at TEXT)"))
    db.execute(_btext("INSERT INTO subscriptions (user_id, plan, status, provider, provider_payment_id, current_period_end, created_at) VALUES (:u,:p,'active','manual','',:e,:c)"),
               {"u": u.id, "p": plan, "e": (_dt.utcnow() + _td(days=30)).isoformat(), "c": _dt.utcnow().isoformat()})
    if hasattr(u, "is_pro"):
        u.is_pro = True
    db.commit()
    return {"ok": True, "plan": plan, "email": email}
