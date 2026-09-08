import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

diag = '''

@router.get("/admin/db-schema")
def admin_db_schema(request: Request, db: Session = Depends(get_db)):
    import os as _os2
    from sqlalchemy import text as _t
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os2.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        tables = db.execute(_t("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
        out = {"tables": [t[0] for t in tables], "billing_orders": []}
        if "billing_orders" in [t[0] for t in tables]:
            cols = db.execute(_t("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'billing_orders'")).fetchall()
            out["billing_orders"] = [{"col": c[0], "type": c[1]} for c in cols]
        return out
    except Exception as e:
        # SQLite fallback
        try:
            tables = db.execute(_t("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            out = {"tables": [t[0] for t in tables], "billing_orders": []}
            if "billing_orders" in [t[0] for t in tables]:
                cols = db.execute(_t("PRAGMA table_info(billing_orders)")).fetchall()
                out["billing_orders"] = [{"col": c[1], "type": c[2]} for c in cols]
            return out
        except Exception as e2:
            return {"error": repr(e2)[:300]}
'''

if '"/admin/db-schema"' not in c:
    c += diag
    print("[ADDED] db-schema diagnostic endpoint")
else:
    print("[SKIP] already present")

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] clean")
except SyntaxError as e:
    print("[ABORT] syntax:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Diagnostic: db-schema endpoint for billing_orders inspection"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
