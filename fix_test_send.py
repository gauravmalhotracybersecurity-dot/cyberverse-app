import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# The exact old test-send function (lines 601-624)
old_test = '''async def nl_test_send(payload: dict, request: Request):
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

# The new provider-aware test-send
new_test = '''async def nl_test_send(payload: dict, request: Request):
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
    provider = _os.environ.get("EMAIL_PROVIDER", "resend").lower()
    
    if provider == "sendgrid":
        from_email = NL_FROM.split("<")[-1].rstrip(">") if "<" in NL_FROM else NL_FROM
        from_name = NL_FROM.split("<")[0].strip() if "<" in NL_FROM else ""
        sendgrid_msg = {
            "personalizations": [{"to": [{"email": email}]}],
            "from": {"email": from_email, "name": from_name},
            "subject": "CyberVerse test",
            "content": [{"type": "text/html", "value": "<p>If you can read this, SendGrid works!</p>"}]
        }
        body = _j.dumps(sendgrid_msg).encode()
        req = _u.Request("https://api.sendgrid.com/v3/mail/send", data=body, method="POST")
        req.add_header("Authorization", "Bearer " + api_key)
        req.add_header("Content-Type", "application/json")
        try:
            with _u.urlopen(req, timeout=15) as r:
                return {"ok": True, "from": NL_FROM, "provider": "sendgrid", "status": r.status}
        except HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            return {"ok": False, "from": NL_FROM, "provider": "sendgrid", "status": e.code, "error_body": error_body[:500]}
        except Exception as e:
            return {"ok": False, "from": NL_FROM, "provider": "sendgrid", "error": repr(e)[:400]}
    else:
        body = _j.dumps({"from": NL_FROM, "to": [email], "subject": "CyberVerse test", "html": "<p>Test</p>"}).encode()
        req = _u.Request("https://api.resend.com/emails", data=body, method="POST")
        req.add_header("Authorization", "Bearer " + api_key)
        req.add_header("Content-Type", "application/json")
        try:
            with _u.urlopen(req, timeout=15) as r:
                resp = _j.loads(r.read())
            return {"ok": True, "from": NL_FROM, "provider": "resend", "response": resp}
        except HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            return {"ok": False, "from": NL_FROM, "provider": "resend", "status": e.code, "error_body": error_body[:500]}
        except Exception as e:
            return {"ok": False, "from": NL_FROM, "provider": "resend", "error": repr(e)[:400]}'''

if old_test in c:
    c = c.replace(old_test, new_test, 1)
    print("[FIX] test-send replaced with SendGrid-aware version")
else:
    print("[ERROR] Could not find exact test-send function")
    raise SystemExit(1)

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: test-send checks EMAIL_PROVIDER and routes to SendGrid"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
