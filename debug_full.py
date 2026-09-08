import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Replace test-send with version that captures FULL Resend response body
old_endpoint = '''@router.post("/newsletter/test-send")
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
        return {"ok": False, "from": NL_FROM, "error": repr(e)[:400]}'''

new_endpoint = '''@router.post("/newsletter/test-send")
async def nl_test_send(payload: dict, request: Request):
    import os as _os, json as _j
    from urllib import request as _u
    from urllib.error import HTTPError
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    email = str((payload or {}).get("email", "")).strip()
    if not email:
        return {"ok": False, "error": "email required"}
    api_key = _os.environ.get("RESEND_API_KEY", "")
    body = _j.dumps({"from": NL_FROM, "to": [email], "subject": "CyberVerse test", "html": "<p>Test</p>"}).encode()
    req = _u.Request("https://api.resend.com/emails", data=body, method="POST")
    req.add_header("Authorization", "Bearer " + api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with _u.urlopen(req, timeout=15) as r:
            resp = _j.loads(r.read())
        return {"ok": True, "from": NL_FROM, "response": resp}
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        return {"ok": False, "from": NL_FROM, "status": e.code, "error_body": error_body[:500], "headers": dict(e.headers)}
    except Exception as e:
        return {"ok": False, "from": NL_FROM, "error": repr(e)[:400]}'''

if old_endpoint in c:
    c = c.replace(old_endpoint, new_endpoint, 1)
    print("[FIX] test-send now captures full Resend error body")
else:
    print("[WARN] old endpoint not found, appending new version")
    c = c.replace('async def nl_test_send', 'async def nl_test_send_OLD')
    c += '\n' + new_endpoint + '\n'

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Debug: capture full Resend error response body"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
