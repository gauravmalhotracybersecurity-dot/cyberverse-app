import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

if '"/billing/verify"' in c:
    print("[SKIP] live billing endpoints already present")
else:
    new_billing = '''@router.post("/billing/checkout")
def billing_checkout(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import os, json as _j, base64
    from urllib import request as _u
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    from plans import PLANS as _P
    plan_key = str((payload or {}).get("plan", ""))
    if plan_key not in _P or plan_key == "free":
        raise HTTPException(status_code=400, detail="Invalid plan")
    key = os.environ.get("RAZORPAY_KEY_ID") or os.environ.get("RAZORPAY_KEY") or ""
    sec = os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or ""
    if not key or not sec:
        return {"status": "coming_soon", "plan": plan_key, "message": "Online payments activate soon - early users are upgraded manually."}
    amount = int(_P[plan_key]["price_inr"]) * 100
    db.execute(_t("CREATE TABLE IF NOT EXISTS billing_orders (order_id TEXT, user_id INTEGER, plan TEXT, created_at TEXT)"))
    data = _j.dumps({"amount": amount, "currency": "INR", "receipt": "rcpt_" + str(user.id) + "_" + plan_key}).encode()
    req = _u.Request("https://api.razorpay.com/v1/orders", data=data, method="POST")
    req.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
    req.add_header("Content-Type", "application/json")
    try:
        with _u.urlopen(req, timeout=20) as r:
            order = _j.loads(r.read())
    except Exception as e:
        return {"status": "error", "error": "Could not create order: " + str(e)}
    db.execute(_t("INSERT INTO billing_orders (order_id, user_id, plan, created_at) VALUES (:o,:u,:p,:c)"),
               {"o": order.get("id"), "u": user.id, "p": plan_key, "c": _dt.utcnow().isoformat()})
    db.commit()
    return {"status": "ok", "order_id": order.get("id"), "key_id": key, "plan": plan_key, "amount": amount,
            "email": user.email, "name": getattr(user, "full_name", "") or ""}


@router.post("/billing/verify")
def billing_verify(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import os, hmac, hashlib
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    p = payload or {}
    order_id = str(p.get("order_id", "")); payment_id = str(p.get("payment_id", "")); signature = str(p.get("signature", ""))
    sec = os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or ""
    calc = hmac.new(sec.encode(), (order_id + "|" + payment_id).encode(), hashlib.sha512).hexdigest()
    if not sec or not hmac.compare_digest(calc, signature):
        return {"ok": False, "error": "Signature verification failed"}
    row = db.execute(_t("SELECT plan FROM billing_orders WHERE order_id=:o"), {"o": order_id}).fetchone()
    plan = row[0] if row else "pro"
    db.execute(_t("CREATE TABLE IF NOT EXISTS subscriptions (user_id INTEGER, plan TEXT, status TEXT, provider TEXT, provider_payment_id TEXT, current_period_end TEXT, created_at TEXT)"))
    db.execute(_t("INSERT INTO subscriptions (user_id, plan, status, provider, provider_payment_id, current_period_end, created_at) VALUES (:u,:p,'active','razorpay',:pid,'lifetime',:c)"),
               {"u": user.id, "p": plan, "pid": payment_id, "c": _dt.utcnow().isoformat()})
    if hasattr(user, "is_pro"):
        user.is_pro = True
    if plan == "premium" and hasattr(user, "is_premium"):
        user.is_premium = True
    db.commit()
    return {"ok": True, "plan": plan}


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


'''
    start = '@router.post("/billing/checkout")'
    end = '@router.post("/billing/activate")'
    i0 = c.find(start); i1 = c.find(end)
    if i0 > -1 and i1 > i0:
        c = c[:i0] + new_billing + c[i1:]
        open(ar, "w", encoding="utf-8").write(c)
        print("[BACKEND] Razorpay live endpoints installed (checkout+verify+webhook)")
    else:
        print("[ERROR] anchors not found - paste me the output")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Payments: install live Razorpay checkout/verify/webhook (stub removal)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
