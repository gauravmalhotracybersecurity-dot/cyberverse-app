import glob, subprocess
skip = ("venv", "node_modules", ".git")
mn = [x for x in glob.glob("**/main.py", recursive=True) if not any(t in x for t in skip) and "backend" in x.replace("\\", "/")]
if mn:
    c = open(mn[0], encoding="utf-8").read()
    if "/api/health/deep" not in c:
        c += '''

@app.get("/api/health/deep")
def health_deep():
    status = {"ok": True}
    try:
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status["db"] = True
    except Exception as e:
        status["db"] = False
        status["db_error"] = repr(e)[:120]
        status["ok"] = False
    return status
'''
        open(mn[0], "w", encoding="utf-8").write(c)
        print("[BACKEND] /api/health/deep added")
    else:
        print("[OK] deep health already present")
else:
    print("[WARN] main.py not found")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Ops: deep health endpoint (DB check) for uptime monitoring"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
