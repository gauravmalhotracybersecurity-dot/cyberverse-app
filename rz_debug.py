import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

dbg = '''@router.post("/billing/checkout")
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


'''
start = '@router.post("/billing/checkout")'
end = '@router.post("/billing/verify")'
i0 = c.find(start); i1 = c.find(end)
if i0 > -1 and i1 > i0:
    c = c[:i0] + dbg + c[i1:]
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] checkout replaced with self-diagnosing version")
else:
    print("[ERROR] anchors not found")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Debug: self-diagnosing billing checkout"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
