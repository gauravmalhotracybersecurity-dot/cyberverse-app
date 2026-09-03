import subprocess

# ---------- 1. CONFIGURABLE PRICING (single source of truth) ----------
plans = '''
PLANS = {
    "free": {
        "name": "Free",
        "price_inr": 0,
        "period": "month",
        "tagline": "Start practicing out loud",
        "limits": {"interviews_per_month": 3, "resume_reviews_per_month": 3, "mentor_messages_per_day": 10},
        "features": ["Limited AI usage", "Basic tools & daily quiz", "Basic certification roadmap", "Weekly league & XP"]
    },
    "pro": {
        "name": "Pro",
        "price_inr": 499,
        "period": "month",
        "tagline": "For serious job seekers",
        "limits": {"interviews_per_month": 100, "resume_reviews_per_month": 50, "mentor_messages_per_day": 200},
        "features": ["High-usage AI interviews & mentor", "Advanced GRC tools & risk assessments", "Resume builder + interview coach", "Advanced certification roadmaps", "Advanced reports & exports"]
    },
    "premium": {
        "name": "Premium",
        "price_inr": 999,
        "period": "month",
        "tagline": "For GRC professionals & teams",
        "limits": {"interviews_per_month": -1, "resume_reviews_per_month": -1, "mentor_messages_per_day": -1},
        "features": ["Everything in Pro", "Advanced GRC assistant & audit assistance", "Advanced templates (SoA, risk register, policies)", "Career assistance & priority features"]
    }
}
'''
open("backend/plans.py", "w", encoding="utf-8").write(plans.strip() + "\n")
print("[CREATED] plans.py (configurable pricing, -1 = unlimited)")

# ---------- 2. BILLING ENDPOINTS (append to analytics_routes) ----------
billing = '''


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
'''
ar = "backend/routers/analytics_routes.py"
c = open(ar, encoding="utf-8").read()
if "def list_plans" not in c:
    open(ar, "w", encoding="utf-8").write(c + billing)
    print("[BACKEND] /plans, /billing/subscription, /checkout, /webhook, /activate added")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 6: configurable pricing + Razorpay-ready subscription architecture"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
