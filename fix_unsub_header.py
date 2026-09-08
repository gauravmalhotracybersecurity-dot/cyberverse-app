import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

anchor = '    url = "https://api.sendgrid.com/v3/mail/send"'
inject = '''    _to = (msg.get("to") or [""])[0]
    sendgrid_msg["headers"] = {
        "List-Unsubscribe": "<https://grcwithgaurav.com/api/analytics/newsletter/unsubscribe?email=" + _to + ">, <mailto:hello@mail.grcwithgaurav.com?subject=unsubscribe>",
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
    }
'''
if anchor in c and "List-Unsubscribe" not in c:
    c = c.replace(anchor, inject + anchor, 1)
    print("[FIX] List-Unsubscribe headers added")
else:
    print("[SKIP] already present or anchor missing")

try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Deliverability: List-Unsubscribe one-click headers (Gmail requirement)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
