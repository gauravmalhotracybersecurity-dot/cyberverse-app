import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# 1. After newsletter subscribe commit: send admin notification
anchor1 = '''    db.execute(_t("INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
    db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
    db.commit()'''
patch1 = anchor1 + '''
    try:
        _nl_send({"from": NL_FROM,
                  "to": [_os.environ.get("ADMIN_NOTIFY_EMAIL") or "gauravmalhotra.cybersecurity@gmail.com"],
                  "subject": "New newsletter subscriber: " + email,
                  "html": "<p><b>" + email + "</b> just subscribed.<br>Source: " + source + "</p><p><a href='https://grcwithgaurav.com/admin-leads'>Open admin</a></p>"})
    except Exception:
        pass'''
if anchor1 in c and "New newsletter subscriber" not in c:
    c = c.replace(anchor1, patch1, 1)
    print("[PATCH] newsletter notification added")

# 2. After B2B lead commit: send admin notification
anchor2 = '''db.execute(_t("INSERT INTO b2b_leads (name, email, company, size, industry, requirement, timeline, created_at) VALUES (:n, :e, :c, :s, :i, :r, :t, :ca)"),
               {"n": p.get("name"), "e": p.get("email"), "c": p.get("company"),
                "s": p.get("size"), "i": p.get("industry"), "r": p.get("requirement"),
                "t": p.get("timeline"), "ca": _dt.utcnow().isoformat()})
    db.commit()'''
patch2 = anchor2 + '''
    try:
        _nl_send({"from": NL_FROM,
                  "to": [_os.environ.get("ADMIN_NOTIFY_EMAIL") or "gauravmalhotra.cybersecurity@gmail.com"],
                  "subject": "New B2B lead: " + str(p.get("company", "")),
                  "html": "<p>New B2B assessment lead:</p><ul><li>Name: " + str(p.get("name", "")) + "</li><li>Email: " + str(p.get("email", "")) + "</li><li>Company: " + str(p.get("company", "")) + "</li><li>Size: " + str(p.get("size", "")) + "</li><li>Timeline: " + str(p.get("timeline", "")) + "</li></ul><p>Requirement: " + str(p.get("requirement", "")) + "</p><p><a href='https://grcwithgaurav.com/admin-leads'>Open admin</a></p>"})
    except Exception:
        pass'''
if anchor2 in c and "New B2B lead" not in c:
    c = c.replace(anchor2, patch2, 1)
    print("[PATCH] B2B lead notification added")

# Compile-check BEFORE writing (the safety net that saves us)
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error, nothing written:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Notifications: subscriber + B2B lead emails to admin (compile-verified)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
