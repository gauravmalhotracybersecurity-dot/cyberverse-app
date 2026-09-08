from fastapi import APIRouter, Depends, HTTPException, Request
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).parent.parent))

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
def track(request: dict, payload: EventIn, db: Session = Depends(get_db)):
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


def _is_admin(user):
    import os
    raw = os.environ.get("ADMIN_EMAIL", "")
    if raw:
        allowed = {x.strip().lower() for x in raw.replace(";", ",").split(",") if x.strip()}
    else:
        allowed = {"gauravmalhotra.cybersecurity@gmail.com", "gaurav_malhotra86@yahoo.com", "gauravmalhotra86@yahoo.com"}
    em = getattr(user, "email", "") or ""
    return em.lower() in allowed


@router.get("/b2b/leads")
def b2b_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    from sqlalchemy import text as _text
    try:
        rows = db.execute(_text("SELECT rowid, name, email, company, size, industry, COALESCE(sales_status,'new'), COALESCE(notes,''), requirement, timeline, created_at FROM b2b_leads ORDER BY rowid DESC LIMIT 500")).fetchall()
    except Exception:
        try:
            db.execute(_text("ALTER TABLE b2b_leads ADD COLUMN sales_status TEXT DEFAULT 'new'"))
            db.execute(_text("ALTER TABLE b2b_leads ADD COLUMN notes TEXT DEFAULT ''"))
            db.commit()
            rows = db.execute(_text("SELECT rowid, name, email, company, size, industry, COALESCE(sales_status,'new'), COALESCE(notes,''), requirement, timeline, created_at FROM b2b_leads ORDER BY rowid DESC LIMIT 500")).fetchall()
        except Exception:
            rows = []
    return [{"id": r[0], "name": r[1], "email": r[2], "company": r[3], "size": r[4], "industry": r[5], "status": r[6], "notes": r[7], "requirement": r[8], "timeline": r[9], "created_at": r[10]} for r in rows]


@router.patch("/b2b/leads/{lead_id}")
def b2b_lead_update(lead_id: int, payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    from sqlalchemy import text as _text
    p = payload or {}
    fields, vals = [], {}
    if "status" in p:
        fields.append("sales_status = :status")
        vals["status"] = str(p["status"])[:30]
    if "notes" in p:
        fields.append("notes = :notes")
        vals["notes"] = str(p["notes"])[:5000]
    if not fields:
        return {"ok": False, "error": "nothing to update"}
    vals["id"] = lead_id
    try:
        db.execute(_text("UPDATE b2b_leads SET " + ", ".join(fields) + " WHERE rowid = :id"), vals)
        db.commit()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.delete("/b2b/leads/{lead_id}")
def b2b_lead_delete(lead_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    from sqlalchemy import text as _text
    try:
        db.execute(_text("DELETE FROM b2b_leads WHERE rowid = :id"), {"id": lead_id})
        db.commit()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}



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
    import os, json as _j, base64, traceback
    from urllib import request as _u
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    try:
        from plans import PLANS as _P
    except Exception as e:
        return {"status": "error", "error": "plans import failed: " + repr(e)}
    try:
        plan_key = str((payload or {}).get("plan", ""))
        if plan_key not in _P or plan_key == "free":
            return {"status": "error", "error": "Invalid plan: " + plan_key}
        key = os.environ.get("RAZORPAY_KEY_ID") or os.environ.get("RAZORPAY_KEY") or ""
        sec = os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or ""
        if not key or not sec:
            return {"status": "coming_soon", "plan": plan_key, "message": "Online payments activate soon."}
        amount = int(_P[plan_key]["price_inr"]) * 100
        try:
            db.execute(_t("CREATE TABLE IF NOT EXISTS billing_orders (order_id TEXT, user_id INTEGER, plan TEXT, created_at TEXT)"))
            db.commit()
        except Exception as e:
            db.rollback()
            return {"status": "error", "error": "db create failed: " + repr(e)}
        data = _j.dumps({"amount": amount, "currency": "INR", "receipt": "rcpt_" + str(user.id) + "_" + plan_key}).encode()
        req = _u.Request("https://api.razorpay.com/v1/orders", data=data, method="POST")
        req.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
        req.add_header("Content-Type", "application/json")
        try:
            with _u.urlopen(req, timeout=20) as r:
                order = _j.loads(r.read())
        except Exception as e:
            return {"status": "error", "error": "razorpay order failed: " + repr(e)}
        try:
            db.execute(_t("INSERT INTO billing_orders (order_id, user_id, plan, created_at) VALUES (:o,:u,:p,:c)"),
                       {"o": order.get("id"), "u": user.id, "p": plan_key, "c": _dt.utcnow().isoformat()})
            db.commit()
        except Exception as e:
            db.rollback()
            return {"status": "error", "error": "db insert failed: " + repr(e)}
        return {"status": "ok", "order_id": order.get("id"), "key_id": key, "plan": plan_key, "amount": amount,
                "email": user.email, "name": getattr(user, "full_name", "") or ""}
    except Exception as e:
        return {"status": "error", "error": repr(e) + " :: " + traceback.format_exc()[-400:]}


@router.post("/billing/verify")
def billing_verify(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import os, hmac, hashlib, json as _j, base64, traceback
    from urllib import request as _u
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    try:
        p = payload or {}
        order_id = str(p.get("order_id", "")); payment_id = str(p.get("payment_id", "")); signature = str(p.get("signature", ""))
        sec = (os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or "").strip()
        key = (os.environ.get("RAZORPAY_KEY_ID") or os.environ.get("RAZORPAY_KEY") or "").strip()
        row = None
        try:
            row = db.execute(_t("SELECT plan, user_id FROM billing_orders WHERE order_id=:o"), {"o": order_id}).fetchone()
        except Exception:
            db.rollback()
        plan = row[0] if row else "pro"
        ok_sig = False
        if sec and signature and signature != "recovery":
            calc = hmac.new(sec.encode(), (order_id + "|" + payment_id).encode(), hashlib.sha512).hexdigest()
            ok_sig = hmac.compare_digest(calc, signature)
        ok_api = False
        api_err = ""
        if not ok_sig and row and row[1] == user.id and key and sec:
            try:
                pid = payment_id
                if not pid:
                    req0 = _u.Request("https://api.razorpay.com/v1/orders/" + order_id + "/payments")
                    req0.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
                    with _u.urlopen(req0, timeout=15) as r0:
                        lst = _j.loads(r0.read())
                    caps = [x for x in (lst.get("items") or []) if x.get("status") == "captured"]
                    if caps:
                        pid = caps[0].get("id")
                if pid:
                    req = _u.Request("https://api.razorpay.com/v1/payments/" + pid)
                req.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
                with _u.urlopen(req, timeout=15) as r:
                    pay = _j.loads(r.read())
                if pay.get("status") == "captured" and pay.get("order_id") == order_id:
                    ok_api = True
                    payment_id = pid
            except Exception as _ae:
                ok_api = False
                api_err = repr(_ae)[:200]
        if not (ok_sig or ok_api):
            return {"ok": False, "error": "Signature verification failed",
                    "diag": {"sec_len": len(sec), "has_sig": bool(signature), "order_owned": bool(row and row[1] == user.id), "api_err": api_err}}
        note = ""
        try:
            db.execute(_t("CREATE TABLE IF NOT EXISTS subscriptions (user_id INTEGER, plan TEXT, status TEXT, provider TEXT, provider_payment_id TEXT, current_period_end TEXT, created_at TEXT)"))
            db.execute(_t("INSERT INTO subscriptions (user_id, plan, status, provider, provider_payment_id, current_period_end, created_at) VALUES (:u,:p,'active','razorpay',:pid,'lifetime',:c)"),
                       {"u": user.id, "p": plan, "pid": payment_id, "c": _dt.utcnow().isoformat()})
        except Exception as e:
            db.rollback()
            note = "subs-full-insert-failed: " + repr(e)[:200]
            try:
                db.execute(_t("INSERT INTO subscriptions (user_id, plan, status, created_at) VALUES (:u,:p,'active',:c)"),
                           {"u": user.id, "p": plan, "c": _dt.utcnow().isoformat()})
                note += " | minimal-insert-ok"
            except Exception as e2:
                db.rollback()
                note += " | minimal-insert-failed: " + repr(e2)[:200]
        if hasattr(user, "is_pro"):
            user.is_pro = True
        if plan == "premium" and hasattr(user, "is_premium"):
            user.is_premium = True
        db.commit()
        return {"ok": True, "plan": plan, "method": "signature" if ok_sig else "api_fallback", "note": note}
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        return {"ok": False, "error": repr(e), "trace": traceback.format_exc()[-500:]}


@router.post("/billing/webhook")
async def billing_webhook(request: Request, db: Session = Depends(get_db)):
    import os, hmac, hashlib, json as _j
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    secret = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")
    body = await request.body()
    sig = request.headers.get("x-razorpay-signature", "")
    if not secret or not hmac.compare_digest(hmac.new(secret.encode(), body, hashlib.sha256).hexdigest(), sig):
        return {"ok": False}
    try:
        ev = _j.loads(body)
    except Exception:
        return {"ok": False}
    if ev.get("event") == "payment.captured":
        ent = ev.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = ent.get("order_id"); payment_id = ent.get("id")
        row = db.execute(_t("SELECT user_id, plan FROM billing_orders WHERE order_id=:o"), {"o": order_id}).fetchone()
        if row:
            db.execute(_t("CREATE TABLE IF NOT EXISTS subscriptions (user_id INTEGER, plan TEXT, status TEXT, provider TEXT, provider_payment_id TEXT, current_period_end TEXT, created_at TEXT)"))
            db.execute(_t("INSERT INTO subscriptions (user_id, plan, status, provider, provider_payment_id, current_period_end, created_at) VALUES (:u,:p,'active','razorpay',:pid,'lifetime',:c)"),
                       {"u": row[0], "p": row[1], "pid": payment_id, "c": _dt.utcnow().isoformat()})
            u = db.query(models.User).filter(models.User.id == row[0]).first()
            if u:
                if hasattr(u, "is_pro"): u.is_pro = True
                if row[1] == "premium" and hasattr(u, "is_premium"): u.is_premium = True
            db.commit()
    return {"ok": True}


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


# ================= NEWSLETTER ENGINE (Resend) =================
import os as _os
import json as _nl_json
from urllib import request as _nl_req
from urllib.parse import quote as _nl_quote
from fastapi.responses import HTMLResponse as _NL_HTML
from fastapi import Request as _NL_Request
from fastapi import HTTPException as _NL_HTTP

NL_FROM = "Gaurav Malhotra <hello@grcwithgaurav.com>"

def _nl_send(messages):
    key = _os.environ.get("RESEND_API_KEY", "")
    if not key:
        return {"ok": False, "error": "RESEND_API_KEY not set"}
    url = "https://api.resend.com/emails/batch" if isinstance(messages, list) else "https://api.resend.com/emails"
    req = _nl_req.Request(url, data=_nl_json.dumps(messages).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    try:
        with _nl_req.urlopen(req, timeout=25) as resp:
            return {"ok": True, "status": getattr(resp, "status", 200)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def _nl_ensure(db):
    from sqlalchemy import text as _t
    db.execute(_t("CREATE TABLE IF NOT EXISTS newsletter_subs (email TEXT UNIQUE, source TEXT, created_at TEXT, unsubscribed INTEGER DEFAULT 0)"))
    db.commit()

KIT_HTML = """<div style="font-family:Arial,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:24px">
<h2 style="color:#00ffcc">Your Free Cybersecurity Starter Kit</h2>
<p>Five artifacts to start your security/GRC journey today - each generated by our free tools:</p>
<ol style="line-height:2.1">
<li><a href="https://grcwithgaurav.com/tools/risk-register-generator" style="color:#00ffcc">ISO 27001 Risk Register (CSV)</a></li>
<li><a href="https://grcwithgaurav.com/tools/iso-gap-assessment" style="color:#00ffcc">ISO 27001 Audit Checklist</a></li>
<li><a href="https://app.grcwithgaurav.com/questions/" style="color:#00ffcc">GRC Interview Questions (practice set)</a></li>
<li><a href="https://grcwithgaurav.com/app.html" style="color:#00ffcc">Cybersecurity Career Roadmap (6 months)</a></li>
<li><a href="https://grcwithgaurav.com/tools/ats-resume-checker" style="color:#00ffcc">Resume Template + ATS check</a></li>
</ol>
<p>Reply to this email if you want a personal nudge in the right direction.<br>- Gaurav</p>
<p style="font-size:12px;color:#888"><a href="https://grcwithgaurav.com/api/analytics/newsletter/unsubscribe?email=__UNSUB__" style="color:#888">Unsubscribe</a></p>
</div>"""

@router.post("/newsletter/subscribe")
def nl_subscribe(payload: dict, db: Session = Depends(get_db)):
    import re as _re
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    try:
        email = str((payload or {}).get("email", "")).strip().lower()[:200]
        source = str((payload or {}).get("source", "footer"))[:50]
        if not _re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", email):
            return {"ok": False, "error": "Invalid email"}
        _nl_ensure(db)
        try:
            db.execute(_t("INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO UPDATE SET unsubscribed=0, source=EXCLUDED.source"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
            db.commit()
        except Exception as db_err:
            db.rollback()
            return {"ok": False, "error": "Database error: " + repr(db_err)[:100]}
        if source == "starter_kit":
            try:
                _nl_send({"from": NL_FROM, "to": [email], "subject": "Your Free Cybersecurity Starter Kit is inside", "html": KIT_HTML.replace("__UNSUB__", _nl_quote(email))})
            except Exception:
                pass
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": repr(e)[:200]}


@router.get("/newsletter/unsubscribe", response_class=_NL_HTML)
def nl_unsubscribe(email: str = "", db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    e = email.strip().lower()
    try:
        _nl_ensure(db)
        db.execute(_t("UPDATE newsletter_subs SET unsubscribed=1 WHERE email=:e"), {"e": e})
        db.commit()
    except Exception:
        pass
    return _NL_HTML("<html><body style='font-family:sans-serif;background:#0a0a0a;color:#e0e0e0;text-align:center;padding:4rem'><h2>You're unsubscribed.</h2><p>No hard feelings - the tools stay free forever.</p><p><a href='https://grcwithgaurav.com/' style='color:#00ffcc'>Back to GRCWithGaurav</a></p></body></html>")

@router.post("/newsletter/send")
def nl_send(payload: dict, request: _NL_Request, db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    secret = _os.environ.get("ADMIN_SECRET", "")
    if not secret or request.headers.get("x-admin-secret") != secret:
        raise _NL_HTTP(status_code=403, detail="Forbidden")
    subject = str((payload or {}).get("subject", ""))[:200]
    body = str((payload or {}).get("body_html", ""))[:200000]
    if not subject or not body:
        return {"ok": False, "error": "subject and body_html required"}
    _nl_ensure(db)
    rows = db.execute(_t("SELECT email FROM newsletter_subs WHERE unsubscribed=0")).fetchall()
    emails = [r[0] for r in rows]
    if not emails:
        return {"ok": True, "sent": 0, "total": 0}
    footer = "<p style='font-size:12px;color:#888'>You receive this because you subscribed at grcwithgaurav.com. <a href='https://grcwithgaurav.com/api/analytics/newsletter/unsubscribe?email=__UNSUB__' style='color:#888'>Unsubscribe</a>.</p>"
    sent = 0
    for i in range(0, len(emails), 50):
        chunk = emails[i:i+50]
        msgs = [{"from": NL_FROM, "to": [e], "subject": subject, "html": body.replace("__UNSUB__", _nl_quote(e)) + footer.replace("__UNSUB__", _nl_quote(e))} for e in chunk]
        r = _nl_send(msgs if len(msgs) > 1 else msgs[0])
        if r.get("ok"):
            sent += len(chunk)
    db.execute(_t("CREATE TABLE IF NOT EXISTS newsletter_log (created_at TEXT, subject TEXT, recipients INTEGER, status TEXT)"))
    db.execute(_t("INSERT INTO newsletter_log (created_at, subject, recipients, status) VALUES (:c,:s,:r,:st)"), {"c": _dt.utcnow().isoformat(), "s": subject, "r": sent, "st": "sent"})
    db.commit()
    return {"ok": True, "sent": sent, "total": len(emails)}


@router.get("/admin/payments")
def admin_payments(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    from sqlalchemy import text as _t
    out = {"subs": [], "abandoned": []}
    try:
        rows = db.execute(_t("SELECT s.user_id, s.plan, s.status, s.provider_payment_id, s.created_at, u.email FROM subscriptions s JOIN users u ON u.id = s.user_id ORDER BY s.created_at DESC LIMIT 300")).fetchall()
        out["subs"] = [{"user_id": r[0], "plan": r[1], "status": r[2], "payment_id": r[3], "created_at": r[4], "email": r[5]} for r in rows]
    except Exception:
        pass
    try:
        rows = db.execute(_t("SELECT o.order_id, o.user_id, o.plan, o.created_at, u.email FROM billing_orders o JOIN users u ON u.id = o.user_id WHERE NOT EXISTS (SELECT 1 FROM subscriptions s WHERE s.user_id = o.user_id AND s.plan = o.plan) ORDER BY o.created_at DESC LIMIT 300")).fetchall()
        out["abandoned"] = [{"order_id": r[0], "user_id": r[1], "plan": r[2], "created_at": r[3], "email": r[4]} for r in rows]
    except Exception:
        pass
    return out


@router.post("/interview/credential")
def mint_credential(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import uuid
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    if not getattr(user, "is_premium", False):
        raise HTTPException(status_code=403, detail="Verified credentials are a Premium feature.")
    p = payload or {}
    cred = uuid.uuid4().hex[:10]
    db.execute(_t("CREATE TABLE IF NOT EXISTS certificates (cred_id TEXT, user_id INTEGER, holder TEXT, role TEXT, score TEXT, created_at TEXT)"))
    db.execute(_t("INSERT INTO certificates (cred_id, user_id, holder, role, score, created_at) VALUES (:c,:u,:h,:r,:s,:t)"),
               {"c": cred, "u": user.id, "h": str(p.get("holder",""))[:120], "r": str(p.get("role",""))[:80],
                "s": str(p.get("score",""))[:10], "t": _dt.utcnow().isoformat()})
    db.commit()
    return {"cred_id": cred, "url": "https://grcwithgaurav.com/c/" + cred}


@router.get("/admin/audience")
def admin_audience(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    out = {"subs": [], "leads": []}
    try:
        rows = db.execute(_t("SELECT email, source, created_at FROM newsletter_subs ORDER BY created_at DESC LIMIT 500")).fetchall()
        out["subs"] = [{"email": r[0], "source": r[1], "created_at": r[2]} for r in rows]
    except Exception:
        pass
    try:
        rows = db.execute(_t("SELECT email, source, created_at FROM leads ORDER BY created_at DESC LIMIT 500")).fetchall()
        out["leads"] = [{"email": r[0], "source": r[1], "created_at": r[2]} for r in rows]
    except Exception:
        pass
    return out
