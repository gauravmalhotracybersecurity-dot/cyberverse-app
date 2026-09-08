import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Add force-resubscribe endpoint
endpoint = '''

@router.post("/admin/force-resubscribe")
def admin_force_resubscribe(payload: dict, db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    email = str((payload or {}).get("email", "")).strip().lower()
    if not email:
        return {"ok": False, "error": "email required"}
    try:
        db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
        db.commit()
        return {"ok": True, "email": email}
    except Exception as e:
        return {"ok": False, "error": repr(e)[:200]}
'''

if '"/admin/force-resubscribe"' not in c:
    c += endpoint
    try:
        compile(c, ar, "exec")
        open(ar, "w", encoding="utf-8").write(c)
        print("[BACKEND] Force-resubscribe endpoint added")
    except SyntaxError as e:
        print("[ABORT] Syntax error:", e)
        raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Admin: force-resubscribe endpoint to fix unsubscribed flag"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
