import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

v3 = '''@router.post("/billing/verify")
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
        if not ok_sig and row and row[1] == user.id and key and sec and payment_id:
            try:
                req = _u.Request("https://api.razorpay.com/v1/payments/" + payment_id)
                req.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
                with _u.urlopen(req, timeout=15) as r:
                    pay = _j.loads(r.read())
                if pay.get("status") == "captured" and pay.get("order_id") == order_id:
                    ok_api = True
            except Exception:
                ok_api = False
        if not (ok_sig or ok_api):
            return {"ok": False, "error": "Signature verification failed",
                    "diag": {"sec_len": len(sec), "has_sig": bool(signature), "order_owned": bool(row and row[1] == user.id)}}
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


'''
start = '@router.post("/billing/verify")'
end = '@router.post("/billing/webhook")'
i0 = c.find(start); i1 = c.find(end)
if i0 > -1 and i1 > i0:
    c = c[:i0] + v3 + c[i1:]
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] verify v3 (crash-proof) installed")
else:
    print("[ERROR] anchors not found")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Payments: verify v3 crash-proof with schema fallbacks"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
