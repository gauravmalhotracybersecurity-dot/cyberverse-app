import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
mr = [x for x in glob.glob("**/main.py", recursive=True) if not any(t in x for t in skip)][0]

# ---------- 1. analytics_routes.py: sweep + endpoint ----------
c = open(ar, encoding="utf-8").read()
addition = '''

CART_HTML = """<div style="font-family:Arial,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:24px">
<h2 style="color:#00ffcc">You left something behind.</h2>
<p>We saved your seat: CyberVerse <strong>__PLAN__</strong> was started but never activated. Your founding-member price stays locked - no pressure, whenever you are ready.</p>
<p style="margin:28px 0"><a href="https://app.grcwithgaurav.com/app.html" style="background:#00ffcc;color:#0a0a0a;padding:12px 22px;text-decoration:none;border-radius:6px;font-weight:bold">Resume checkout</a></p>
<p>Stuck on payment or unsure which plan fits? Reply to this email - Gaurav answers personally within a day.</p>
<p style="font-size:12px;color:#888">One reminder only - you will not hear about this again. <a href="https://grcwithgaurav.com/api/analytics/newsletter/unsubscribe?email=__UNSUB__" style="color:#888">Unsubscribe</a>.</p>
</div>"""

_CART_LAST = [0.0]


def cart_sweep(db, min_hours=24.0):
    from sqlalchemy import text as _t
    from datetime import datetime as _dt, timedelta as _td
    db.execute(_t("CREATE TABLE IF NOT EXISTS cart_recovery (order_id TEXT PRIMARY KEY, email TEXT, sent_at TEXT)"))
    db.commit()
    now = _dt.utcnow()
    old = (now - _td(hours=min_hours)).isoformat()
    week = (now - _td(days=7)).isoformat()
    rows = db.execute(_t("SELECT o.order_id, o.user_id, o.plan, o.created_at, u.email FROM billing_orders o JOIN users u ON u.id = o.user_id WHERE NOT EXISTS (SELECT 1 FROM subscriptions s WHERE s.user_id = o.user_id AND s.plan = o.plan) AND o.created_at < :old AND o.created_at > :week ORDER BY o.created_at DESC LIMIT 50"), {"old": old, "week": week}).fetchall()
    sent = 0
    for r in rows:
        order_id, plan, email = r[0], r[2], r[4]
        if db.execute(_t("SELECT 1 FROM cart_recovery WHERE order_id=:o"), {"o": order_id}).fetchone():
            continue
        html = CART_HTML.replace("__PLAN__", str(plan).title()).replace("__UNSUB__", str(email))
        res = _nl_send({"from": NL_FROM, "to": [email], "subject": "Your CyberVerse " + str(plan).title() + " seat is still held", "html": html})
        db.execute(_t("INSERT INTO cart_recovery (order_id, email, sent_at) VALUES (:o,:e,:s) ON CONFLICT (order_id) DO NOTHING"), {"o": order_id, "e": email, "s": _dt.utcnow().isoformat()})
        db.commit()
        if isinstance(res, dict) and res.get("ok"):
            sent += 1
    return {"ok": True, "found": len(rows), "sent": sent}


def cart_sweep_throttled(db):
    import time as _time
    now = _time.time()
    if now - _CART_LAST[0] < 86400:
        return {"ok": True, "skipped": True}
    _CART_LAST[0] = now
    return cart_sweep(db)


@router.post("/admin/recover-carts")
def admin_recover_carts(payload: dict, request: Request, db: Session = Depends(get_db)):
    import os as _os2
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os2.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    hours = 24.0
    try:
        hours = float((payload or {}).get("min_hours", 24))
    except Exception:
        hours = 24.0
    return cart_sweep(db, min_hours=hours)
'''

if "def cart_sweep(" not in c:
    c += addition
    print("[ADDED] cart sweep + admin trigger")
else:
    print("[SKIP] sweep already present")

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] analytics_routes clean")
except SyntaxError as e:
    print("[ABORT] analytics syntax:", e)
    raise SystemExit(1)

# ---------- 2. main.py: health hook ----------
m = open(mr, encoding="utf-8").read()
anchor = '@app.get("/api/health")\ndef health():\n'
hook = anchor + '''    try:
        import importlib as _il
        try:
            _ar = _il.import_module("routers.analytics_routes")
        except Exception:
            _ar = _il.import_module("backend.routers.analytics_routes")
        try:
            from database import SessionLocal as _SL
        except Exception:
            from backend.database import SessionLocal as _SL
        _cdb = _SL()
        try:
            _ar.cart_sweep_throttled(_cdb)
        finally:
            _cdb.close()
    except Exception:
        pass
'''
if anchor in m and "cart_sweep_throttled" not in m:
    m = m.replace(anchor, hook, 1)
    print("[ADDED] health hook scheduler")
else:
    print("[SKIP] health hook already present or anchor missing")

try:
    compile(m, mr, "exec")
    open(mr, "w", encoding="utf-8").write(m)
    print("[COMPILE] main clean")
except SyntaxError as e:
    print("[ABORT] main syntax:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Revenue: abandoned-cart recovery emails (24h sweep + admin trigger)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
