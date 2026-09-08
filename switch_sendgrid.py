import glob, subprocess, re
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Find the _nl_send function and replace it with SendGrid version
old_nl_send = '''def _nl_send(messages):
    key = _os.environ.get("RESEND_API_KEY", "")
    if not key:
        return {"ok": False, "error": "RESEND_API_KEY not set"}
    url = "https://api.resend.com/emails/batch" if isinstance(messages, list) else "https://api.resend.com/emails"
    req = _nl_req.Request(url, data=_nl_json.dumps(messages).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": "cyberverse-app/1.0"}, method="POST")
    try:
        with _nl_req.urlopen(req, timeout=25) as resp:
            return {"ok": True, "status": getattr(resp, "status", 200)}
    except Exception as e:
        return {"ok": False, "error": str(e)}'''

new_nl_send = '''def _nl_send(messages):
    key = _os.environ.get("RESEND_API_KEY", "")
    provider = _os.environ.get("EMAIL_PROVIDER", "resend").lower()
    if not key:
        return {"ok": False, "error": "RESEND_API_KEY not set"}
    
    if provider == "sendgrid":
        # SendGrid API v3
        if isinstance(messages, list):
            # Batch send
            results = []
            for msg in messages:
                r = _nl_send_single_sendgrid(msg, key)
                results.append(r)
            return {"ok": all(r.get("ok") for r in results), "results": results}
        else:
            return _nl_send_single_sendgrid(messages, key)
    else:
        # Original Resend API (fallback)
        url = "https://api.resend.com/emails/batch" if isinstance(messages, list) else "https://api.resend.com/emails"
        req = _nl_req.Request(url, data=_nl_json.dumps(messages).encode("utf-8"),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
        try:
            with _nl_req.urlopen(req, timeout=25) as resp:
                return {"ok": True, "status": getattr(resp, "status", 200)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

def _nl_send_single_sendgrid(msg, key):
    """Send single email via SendGrid"""
    # Convert Resend format to SendGrid format
    sendgrid_msg = {
        "personalizations": [{"to": [{"email": e} for e in msg.get("to", [])]}],
        "from": {"email": msg.get("from", "").split("<")[-1].rstrip(">") if "<" in msg.get("from", "") else msg.get("from", ""),
                 "name": msg.get("from", "").split("<")[0].strip() if "<" in msg.get("from", "") else ""},
        "subject": msg.get("subject", ""),
        "content": [{"type": "text/html", "value": msg.get("html", "")}]
    }
    
    url = "https://api.sendgrid.com/v3/mail/send"
    req = _nl_req.Request(url, data=_nl_json.dumps(sendgrid_msg).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json"
        }, method="POST")
    try:
        with _nl_req.urlopen(req, timeout=25) as resp:
            return {"ok": True, "status": getattr(resp, "status", 202)}
    except Exception as e:
        return {"ok": False, "error": str(e)}'''

if old_nl_send in c:
    c = c.replace(old_nl_send, new_nl_send, 1)
    print("[FIX] _nl_send replaced with SendGrid version")
else:
    print("[WARN] Could not find exact _nl_send pattern, trying regex")
    # Try to find and replace with regex
    pattern = r'def _nl_send\(messages\):.*?(?=\n    def |\nclass |\Z)'
    if re.search(pattern, c, re.DOTALL):
        c = re.sub(pattern, new_nl_send + '\n', c, flags=re.DOTALL)
        print("[FIX] _nl_send replaced via regex")
    else:
        print("[ERROR] Could not find _nl_send function")
        raise SystemExit(1)

# Update test-send to use SendGrid format
old_test = '''        api_key = _os.environ.get("RESEND_API_KEY", "")
        body = _j.dumps({"from": NL_FROM, "to": [email], "subject": "CyberVerse test", "html": "<p>Test</p>"}).encode()
        req = _u.Request("https://api.resend.com/emails", data=body, method="POST")
        req.add_header("Authorization", "Bearer " + api_key)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        req.add_header("Accept-Language", "en-US,en;q=0.9")
        req.add_header("Origin", "https://grcwithgaurav.com")
        req.add_header("Referer", "https://grcwithgaurav.com/")
        try:
            with _u.urlopen(req, timeout=15) as r:
                resp = _j.loads(r.read())
            return {"ok": True, "from": NL_FROM, "response": resp}'''

new_test = '''        api_key = _os.environ.get("RESEND_API_KEY", "")
        provider = _os.environ.get("EMAIL_PROVIDER", "resend").lower()
        
        if provider == "sendgrid":
            # SendGrid format
            from_email = NL_FROM.split("<")[-1].rstrip(">") if "<" in NL_FROM else NL_FROM
            from_name = NL_FROM.split("<")[0].strip() if "<" in NL_FROM else ""
            sendgrid_msg = {
                "personalizations": [{"to": [{"email": email}]}],
                "from": {"email": from_email, "name": from_name},
                "subject": "CyberVerse test",
                "content": [{"type": "text/html", "value": "<p>Test</p>"}]
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
                return {"ok": False, "from": NL_FROM, "provider": "sendgrid", "status": e.code, "error": error_body[:500]}
        else:
            # Resend format (fallback)
            body = _j.dumps({"from": NL_FROM, "to": [email], "subject": "CyberVerse test", "html": "<p>Test</p>"}).encode()
            req = _u.Request("https://api.resend.com/emails", data=body, method="POST")
            req.add_header("Authorization", "Bearer " + api_key)
            req.add_header("Content-Type", "application/json")
            try:
                with _u.urlopen(req, timeout=15) as r:
                    resp = _j.loads(r.read())
                return {"ok": True, "from": NL_FROM, "provider": "resend", "response": resp}'''

if old_test in c:
    c = c.replace(old_test, new_test, 1)
    print("[FIX] test-send updated for SendGrid")
else:
    print("[WARN] Could not find test-send pattern")

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Switch to SendGrid email provider (bypass Cloudflare 1010)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
