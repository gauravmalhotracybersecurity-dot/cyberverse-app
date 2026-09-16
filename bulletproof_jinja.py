import subprocess, re

print("=== APPLYING BULLETPROOF JINJA FALLBACK ===\n")

p = "backend/templates/base.html"
c = open(p, encoding="utf-8").read()

# Find the current canonical block
m = re.search(r'{% block canonical %}.*?{% endblock %}', c, re.DOTALL)
if m:
    old_block = m.group(0)
    print(f"Found: {old_block}")
    
    # Replace with pure Jinja2 logic (no Python method calls)
    new_block = '''{% block canonical %}{% set clean_path = request.url.path %}{% if clean_path != '/' and clean_path.endswith('/') %}{% set clean_path = clean_path[:-1] %}{% endif %}https://grcwithgaurav.com{{ clean_path }}{% endblock %}'''
    
    c = c.replace(old_block, new_block)
    open(p, "w", encoding="utf-8").write(c)
    print("[FIXED] Replaced with pure Jinja2 logic")
else:
    print("[ERROR] Canonical block not found")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: bulletproof Jinja2 canonical slash stripping"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
