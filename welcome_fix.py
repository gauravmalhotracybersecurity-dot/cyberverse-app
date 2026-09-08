import glob, os, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
n = 0

# 1. Welcome email template
welcome = '''WELCOME_HTML = """<div style="font-family:Arial,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:24px">
<h2 style="color:#00ffcc">You're on the list. Welcome.</h2>
<p>Every Monday: one email, three links - the best free GRC/cybersecurity guides, tools and one honest career take. No spam, ever.</p>
<p><strong>Start here (all free):</strong></p>
<ol style="line-height:2.1">
<li><a href="https://grcwithgaurav.com/tools" style="color:#00ffcc">10 free GRC tools (risk register, ISO gap assessment, ATS checker)</a></li>
<li><a href="https://grcwithgaurav.com/app.html" style="color:#00ffcc">AI Mock Interview Coach - free practice session</a></li>
<li><a href="https://grcwithgaurav.com/learn/how-to-start-grc-career" style="color:#00ffcc">How to Start a GRC Career in 2026 (no IT background)</a></li>
</ol>
<p>Reply to this email any time - it reaches Gaurav directly.<br>- Gaurav</p>
<p style="font-size:12px;color:#888"><a href="https://grcwithgaurav.com/api/analytics/newsletter/unsubscribe?email=__UNSUB__" style="color:#888">Unsubscribe</a></p>
</div>"""


'''
anchor_sub = '@router.post("/newsletter/subscribe")'
if "WELCOME_HTML" not in c and anchor_sub in c:
    c = c.replace(anchor_sub, welcome + anchor_sub, 1)
    n += 1
    print("[ADDED] WELCOME_HTML template")

# 2. Send welcome email after subscribe
old_block = '''        if source == "starter_kit":
            try:
                _nl_send({"from": NL_FROM, "to": [email], "subject": "Your Free Cybersecurity Starter Kit is inside", "html": KIT_HTML.replace("__UNSUB__", _nl_quote(email))})
            except Exception:
                pass
        return {"ok": True}'''
new_block = '''        if source == "starter_kit":
            try:
                _nl_send({"from": NL_FROM, "to": [email], "subject": "Your Free Cybersecurity Starter Kit is inside", "html": KIT_HTML.replace("__UNSUB__", _nl_quote(email))})
            except Exception:
                pass
        else:
            try:
                _nl_send({"from": NL_FROM, "to": [email], "subject": "Welcome to GRCWithGaurav", "html": WELCOME_HTML.replace("__UNSUB__", email)})
            except Exception:
                pass
        return {"ok": True}'''
if old_block in c:
    c = c.replace(old_block, new_block, 1)
    n += 1
    print("[ADDED] welcome email send after subscribe")

print("[TOTAL] patches:", n)
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Newsletter: instant welcome email on subscribe"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
