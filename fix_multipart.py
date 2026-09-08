import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
n = 0

# 1. Add plain-text helper
helper = '''def _nl_plain(html):
    import re as _re2
    return _re2.sub(r"<[^>]+>", " ", html or "")[:3000]


'''
anchor = "def _nl_send_single_sendgrid"
if anchor in c and "_nl_plain" not in c:
    c = c.replace(anchor, helper + anchor, 1); n += 1

# 2. Batch/single send: add text/plain part
old1 = '"content": [{"type": "text/html", "value": msg.get("html", "")}]'
new1 = '"content": [{"type": "text/plain", "value": _nl_plain(msg.get("html", ""))}, {"type": "text/html", "value": msg.get("html", "")}]'
if old1 in c:
    c = c.replace(old1, new1, 1); n += 1

# 3. Test-send: add text/plain part
old2 = '"content": [{"type": "text/html", "value": "<p>If you can read this, SendGrid works!</p>"}]'
new2 = '"content": [{"type": "text/plain", "value": "If you can read this, SendGrid works!"}, {"type": "text/html", "value": "<p>If you can read this, SendGrid works!</p>"}]'
if old2 in c:
    c = c.replace(old2, new2, 1); n += 1

print("[PATCH] changes applied:", n)
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Deliverability: multipart emails (plain text + HTML) to beat spam filters"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
