import subprocess, re, os

print("=== FIXING HARDCODED CANONICAL BLOCKS IN TOOL TEMPLATES ===\n")

tools_dir = "backend/templates/tools"
fixed = 0

for fname in sorted(os.listdir(tools_dir)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    path = os.path.join(tools_dir, fname)
    c = open(path, encoding="utf-8").read()
    
    # Strip trailing slash inside {% block canonical %}...{% endblock %}
    new_c, n = re.subn(
        r'(\{%\s*block canonical\s*%\}\s*https://grcwithgaurav\.com/tools/[a-z0-9-]+)/(\s*\{%\s*endblock\s*%\})',
        r'\1\2',
        c
    )
    
    if n:
        open(path, "w", encoding="utf-8").write(new_c)
        m = re.search(r'{% block canonical %}.*?{% endblock %}', new_c)
        print(f"[FIXED] {fname} -> {m.group(0)}")
        fixed += 1
    else:
        print(f"[OK]    {fname} (no slash in block)")

print(f"\nFixed {fixed} of 9 tool templates")

# Local sanity check: parse all templates
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("backend/templates"))
for fname in sorted(os.listdir(tools_dir)):
    if fname.endswith(".html"):
        try:
            env.get_template(f"tools/{fname}")
        except Exception as e:
            print(f"[BROKEN] tools/{fname}: {e}")
            raise SystemExit(1)
print("All tool templates parse OK")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: strip trailing slash from hardcoded canonical blocks in all 9 tool templates"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
