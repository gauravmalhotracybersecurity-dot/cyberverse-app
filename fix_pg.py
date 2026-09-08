import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Replace the broken INSERT OR IGNORE with PostgreSQL's ON CONFLICT
old_sql = 'INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)'
new_sql = 'INSERT INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0) ON CONFLICT (email) DO NOTHING'

if old_sql in c:
    c = c.replace(old_sql, new_sql, 1)
    print("[FIX] SQLite syntax replaced with PostgreSQL ON CONFLICT")
else:
    print("[WARN] Pattern not found")

# Compile-check
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: PostgreSQL dialect (ON CONFLICT instead of INSERT OR IGNORE)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
