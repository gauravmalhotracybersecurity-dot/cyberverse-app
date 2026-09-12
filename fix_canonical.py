import subprocess

print("=== FIXING CANONICAL TAGS ===\n")

# Fix /learn
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
if "{% block canonical %}/learn{% endblock %}" in learn:
    learn = learn.replace(
        "{% block canonical %}/learn{% endblock %}",
        "{% block canonical %}https://grcwithgaurav.com/learn{% endblock %}"
    )
    open("backend/templates/learn/index.html", "w", encoding="utf-8").write(learn)
    print("[FIX] /learn: updated canonical to full URL")
else:
    print("[CHECK] /learn canonical block:")
    import re
    match = re.search(r'{% block canonical %}.*?{% endblock %}', learn)
    if match:
        print(f"  Found: {match.group(0)}")

# Fix /resources
res = open("backend/templates/resources.html", encoding="utf-8").read()
if "{% block canonical %}/resources{% endblock %}" in res:
    res = res.replace(
        "{% block canonical %}/resources{% endblock %}",
        "{% block canonical %}https://grcwithgaurav.com/resources{% endblock %}"
    )
    open("backend/templates/resources.html", "w", encoding="utf-8").write(res)
    print("[FIX] /resources: updated canonical to full URL")
else:
    print("[CHECK] /resources canonical block:")
    match = re.search(r'{% block canonical %}.*?{% endblock %}', res)
    if match:
        print(f"  Found: {match.group(0)}")

# Commit and push
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: canonical tags use full URLs for /learn and /resources"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
