import glob, subprocess, os
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

endpoint = '''

@router.post("/newsletter/test-send")
async def nl_test_send(payload: dict, request: Request):
    import os as _os
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    email = str((payload or {}).get("email", "")).strip()
    if not email:
        return {"ok": False, "error": "email required"}
    try:
        result = _nl_send({"from": NL_FROM, "to": [email],
                           "subject": "CyberVerse test email",
                           "html": "<p>If you can read this, the newsletter pipeline works.</p>"})
        return {"ok": True, "from": NL_FROM, "result": str(result)[:300]}
    except Exception as e:
        return {"ok": False, "from": NL_FROM, "error": repr(e)[:400]}
'''

if '"/newsletter/test-send"' not in c:
    c += endpoint
    try:
        compile(c, ar, "exec")
        open(ar, "w", encoding="utf-8").write(c)
        print("[BACKEND] test-send debug endpoint added")
    except SyntaxError as e:
        print("[ABORT] Syntax error:", e)
        raise SystemExit(1)
else:
    print("[OK] already present")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Debug: newsletter test-send endpoint exposes Resend errors"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
