import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Replace the broken two-step with a single PostgreSQL upsert
old_sql = '''INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO NOTHING'''
new_sql = '''INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO UPDATE SET unsubscribed=0, source=EXCLUDED.source'''

if old_sql in c:
    c = c.replace(old_sql, new_sql, 1)
    print("[FIX] PostgreSQL upsert (INSERT ... ON CONFLICT DO UPDATE)")
else:
    print("[WARN] Pattern not found")

# Remove the now-redundant UPDATE statement
old_update = '''        try:
            db.execute(_t("INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO UPDATE SET unsubscribed=0, source=EXCLUDED.source"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
            db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
            db.commit()'''
new_update = '''        try:
            db.execute(_t("INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO UPDATE SET unsubscribed=0, source=EXCLUDED.source"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
            db.commit()'''

if old_update in c:
    c = c.replace(old_update, new_update, 1)
    print("[FIX] Redundant UPDATE removed")

# Compile-check
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: PostgreSQL upsert ensures re-subscribe sets unsubscribed=0"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
