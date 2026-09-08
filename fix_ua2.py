import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Fix 1: _nl_send function (line ~397) - add User-Agent to headers dict
old1 = '        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")'
new1 = '        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": "cyberverse-app/1.0"}, method="POST")'

if old1 in c:
    c = c.replace(old1, new1, 1)
    print("[FIX 1] User-Agent added to _nl_send")
else:
    print("[WARN] _nl_send pattern not found")

# Fix 2: nl_test_send function (line ~575) - add User-Agent after Content-Type
old2 = '    req.add_header("Content-Type", "application/json")\n        try:'
new2 = '    req.add_header("Content-Type", "application/json")\n        req.add_header("User-Agent", "cyberverse-app/1.0")\n        try:'

if old2 in c:
    c = c.replace(old2, new2, 1)
    print("[FIX 2] User-Agent added to nl_test_send")
else:
    # Try with different indent
    old2b = 'req.add_header("Content-Type", "application/json")\n        try:'
    new2b = 'req.add_header("Content-Type", "application/json")\n        req.add_header("User-Agent", "cyberverse-app/1.0")\n        try:'
    if old2b in c:
        c = c.replace(old2b, new2b, 1)
        print("[FIX 2b] User-Agent added to nl_test_send")
    else:
        print("[WARN] nl_test_send pattern not found")

# Compile check
try:
    compile(c, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: User-Agent header on Resend API calls (Cloudflare 1010 bypass)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
