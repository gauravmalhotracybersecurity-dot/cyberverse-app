import glob, subprocess
sr = glob.glob("backend/routers/site_routes.py")[0]
c = open(sr, encoding="utf-8").read()

# Fix line 2: add Depends to the import
old = "from fastapi import APIRouter, Request, HTTPException"
new = "from fastapi import APIRouter, Request, HTTPException, Depends"

if old in c and new not in c:
    c = c.replace(old, new, 1)
    print("[FIX] Added Depends to fastapi imports")
else:
    print("[SKIP] Already fixed or pattern not found")

open(sr, "w", encoding="utf-8").write(c)
print("[COMPILE] File updated")

# Verify it compiles
try:
    compile(c, sr, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: add Depends import to site_routes (restores all frontend routes)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED - Render will redeploy in ~60s")
