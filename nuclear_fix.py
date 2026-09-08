import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Find and completely replace the nl_subscribe function
import re

# Pattern to find the entire function
pattern = r'@router\.post\("/newsletter/subscribe"\)\s*\n\s*def nl_subscribe\([^)]+\):[^}]+?(?=\n@router|\nclass |\Z)'

clean_function = '''@router.post("/newsletter/subscribe")
def nl_subscribe(payload: dict, db: Session = Depends(get_db)):
    import re as _re
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    email = str((payload or {}).get("email", "")).strip().lower()[:200]
    source = str((payload or {}).get("source", "footer"))[:50]
    if not _re.match(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$", email):
        return {"ok": False, "error": "Invalid email"}
    _nl_ensure(db)
    db.execute(_t("INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
    db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
    db.commit()
    if source == "starter_kit":
        _nl_send({"from": NL_FROM, "to": [email], "subject": "Your Free Cybersecurity Starter Kit is inside", "html": KIT_HTML.replace("__UNSUB__", _nl_quote(email))})
    return {"ok": True}

'''

# Find the function
match = re.search(pattern, c, re.DOTALL)
if match:
    print("[FOUND] nl_subscribe function, replacing completely")
    c = c[:match.start()] + clean_function + c[match.end():]
else:
    print("[WARN] Could not find nl_subscribe function pattern")
    # Fallback: find @router.post("/newsletter/subscribe") and replace until next @router
    start = c.find('@router.post("/newsletter/subscribe")')
    if start > -1:
        next_router = c.find('\n@router', start + 1)
        if next_router == -1:
            next_router = len(c)
        print(f"[FALLBACK] Replacing from {start} to {next_router}")
        c = c[:start] + clean_function + c[next_router:]

open(ar, "w", encoding="utf-8").write(c)
print("[BACKEND] nl_subscribe completely rewritten")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: rewrite nl_subscribe function to eliminate syntax error"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
