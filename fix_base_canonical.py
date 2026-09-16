import subprocess

print("=== FIXING CANONICAL SOURCE IN BASE.HTML ===\n")

p = "backend/templates/base.html"
c = open(p, encoding="utf-8").read()

# The issue: request.url.path includes the trailing slash for tool routes.
# Fix: Strip it using rstrip("/").
old = '{% block canonical %}https://grcwithgaurav.com{{ request.url.path }}{% endblock %}'
new = '{% block canonical %}https://grcwithgaurav.com{{ request.url.path.rstrip("/") }}{% endblock %}'

if old in c:
    c = c.replace(old, new)
    open(p, "w", encoding="utf-8").write(c)
    print("[FIXED] base.html: default canonical now strips trailing slash")
else:
    print("[CHECK] Pattern not found. Checking current content...")
    import re
    m = re.search(r'{% block canonical %}.*?{% endblock %}', c)
    if m: print(f"  Found: {m.group(0)}")

# Commit and push
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: strip trailing slash from default canonical in base.html"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
