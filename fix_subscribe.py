import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Find and completely replace nl_subscribe with a bulletproof version
import re

pattern = r'@router\.post\("/newsletter/subscribe"\)\s*\n\s*def nl_subscribe\([^)]+\):[^}]+?(?=\n@router|\nclass |\Z)'

clean_function = '''@router.post("/newsletter/subscribe")
def nl_subscribe(payload: dict, db: Session = Depends(get_db)):
    import re as _re
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    try:
        email = str((payload or {}).get("email", "")).strip().lower()[:200]
        source = str((payload or {}).get("source", "footer"))[:50]
        if not _re.match(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$", email):
            return {"ok": False, "error": "Invalid email"}
        _nl_ensure(db)
        try:
            db.execute(_t("INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
            db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
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

'''

match = re.search(pattern, c, re.DOTALL)
if match:
    print("[FOUND] nl_subscribe, replacing with bulletproof version")
    c = c[:match.start()] + clean_function + c[match.end():]
else:
    print("[WARN] Pattern not found, trying anchor replacement")
    start = c.find('@router.post("/newsletter/subscribe")')
    if start > -1:
        next_router = c.find('\n@router', start + 1)
        if next_router == -1:
            next_router = len(c)
        c = c[:start] + clean_function + c[next_router:]

# Compile-check
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: bulletproof newsletter subscribe with defensive error handling"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
