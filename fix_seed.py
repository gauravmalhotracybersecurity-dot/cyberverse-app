import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Replace the broken seed endpoint with corrected version
old_seed = '''@router.post("/admin/seed-abandoned")
def admin_seed_abandoned(payload: dict, request: Request, db: Session = Depends(get_db)):
    import os as _os2, uuid as _uuid
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os2.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    email = str((payload or {}).get("email", "")).strip()
    plan = str((payload or {}).get("plan", "pro")).strip() or "pro"
    if not email:
        return {"ok": False, "error": "email required"}
    # Find user
    row = db.execute(_t("SELECT id FROM users WHERE email=:e"), {"e": email}).fetchone()
    if not row:
        return {"ok": False, "error": "user not found - subscribe via /api/auth/register first"}
    user_id = row[0]
    order_id = "test_" + str(_uuid.uuid4())[:12]
    # Insert order dated 48h ago so it clears the 24h threshold
    from datetime import timedelta as _td
    old = (_dt.utcnow() - _td(hours=48)).isoformat()
    db.execute(_t("INSERT INTO billing_orders (order_id, user_id, plan, amount, status, created_at) VALUES (:o,:u,:p,:a,:s,:c)"),
               {"o": order_id, "u": user_id, "p": plan, "a": 499, "s": "created", "c": old})
    db.commit()
    return {"ok": True, "order_id": order_id, "user_id": user_id, "plan": plan, "created_at": old}'''

new_seed = '''@router.post("/admin/seed-abandoned")
def admin_seed_abandoned(payload: dict, request: Request, db: Session = Depends(get_db)):
    import os as _os2, uuid as _uuid
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os2.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    email = str((payload or {}).get("email", "")).strip()
    plan = str((payload or {}).get("plan", "pro")).strip() or "pro"
    if not email:
        return {"ok": False, "error": "email required"}
    # Find user
    row = db.execute(_t("SELECT id FROM users WHERE email=:e"), {"e": email}).fetchone()
    if not row:
        return {"ok": False, "error": "user not found - subscribe via /api/auth/register first"}
    user_id = row[0]
    order_id = "test_" + str(_uuid.uuid4())[:12]
    # Insert order dated 48h ago so it clears the 24h threshold
    from datetime import timedelta as _td
    old = (_dt.utcnow() - _td(hours=48)).isoformat()
    db.execute(_t("INSERT INTO billing_orders (user_id, order_id, plan, created_at) VALUES (:u,:o,:p,:c)"),
               {"u": user_id, "o": order_id, "p": plan, "c": old})
    db.commit()
    return {"ok": True, "order_id": order_id, "user_id": user_id, "plan": plan, "created_at": old}'''

if old_seed in c:
    c = c.replace(old_seed, new_seed, 1)
    print("[FIX] seed-abandoned corrected (removed amount/status columns)")
else:
    print("[WARN] pattern not found, trying line-by-line fix")
    lines = c.split('\n')
    for i, line in enumerate(lines):
        if 'INSERT INTO billing_orders' in line and 'amount' in line:
            lines[i] = '    db.execute(_t("INSERT INTO billing_orders (user_id, order_id, plan, created_at) VALUES (:u,:o,:p,:c)"),'
            if i+1 < len(lines):
                lines[i+1] = '               {"u": user_id, "o": order_id, "p": plan, "c": old})'
            print("[FIX] line-by-line replacement done")
            break
    c = '\n'.join(lines)

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] clean")
except SyntaxError as e:
    print("[ABORT] syntax:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: seed-abandoned uses correct billing_orders columns"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
