import subprocess, re

print("=== FIXING CANONICAL BLOCKS ===\n")

# Fix /learn
learn_path = "backend/templates/learn/index.html"
learn = open(learn_path, encoding="utf-8").read()
old_learn = "{% block canonical %}{{ base_url }}/learn{% endblock %}"
new_learn = "{% block canonical %}https://grcwithgaurav.com/learn{% endblock %}"
if old_learn in learn:
    learn = learn.replace(old_learn, new_learn)
    open(learn_path, "w", encoding="utf-8").write(learn)
    print("[FIX] /learn: hardcoded full URL in canonical block")
else:
    print("[SKIP] /learn canonical block already fixed or not found")

# Fix /resources
res_path = "backend/templates/resources.html"
res = open(res_path, encoding="utf-8").read()
old_res = "{% block canonical %}{{ base_url }}/resources{% endblock %}"
new_res = "{% block canonical %}https://grcwithgaurav.com/resources{% endblock %}"
if old_res in res:
    res = res.replace(old_res, new_res)
    open(res_path, "w", encoding="utf-8").write(res)
    print("[FIX] /resources: hardcoded full URL in canonical block")
else:
    print("[SKIP] /resources canonical block already fixed or not found")

# Check for any other {{ base_url }} usage in these files that might be broken
for p in [learn_path, res_path]:
    c = open(p, encoding="utf-8").read()
    if "{{ base_url }}" in c:
        print(f"\n[WARN] {p} still contains {c.count('{{ base_url }}')} references to base_url")
    else:
        print(f"\n[OK] {p} has no broken base_url references")

print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: hardcode full URLs in canonical blocks for /learn and /resources"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
