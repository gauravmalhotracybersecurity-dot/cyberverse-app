import subprocess, re, os

p = "backend/templates/resources.html"
res = open(p, encoding="utf-8").read()

print("=== CLEANING /resources BOOKS CARD PLACEMENT ===")

# 1. Remove any existing misplaced Ebooks & Playbooks card
pattern = re.compile(
    r'\n?<div class="card"[^>]*>\s*'
    r'<h3[^>]*>Ebooks &amp; Playbooks</h3>.*?'
    r'See All Books.*?'
    r'</div>\s*',
    re.DOTALL
)

res2, n = pattern.subn("\n", res)
print(f"Removed existing Ebooks card blocks: {n}")
res = res2

# 2. Insert clean card before the LAST endblock, which should be content endblock
books_card = '''
<div class="card" style="padding:1.5rem;margin-top:1.5rem">
 <h3 style="margin-top:0">Ebooks &amp; Playbooks</h3>
 <p style="color:var(--muted);margin:.5rem 0 1rem">Three practical playbooks for GRC and AI in security careers.</p>
 <a href="/books" class="btn-primary" style="display:inline-block">See All Books &rarr;</a>
</div>
'''

last_endblock = res.rfind("{% endblock %}")
if last_endblock < 0:
    print("[ERROR] Could not find final {% endblock %}")
    raise SystemExit(1)

res = res[:last_endblock] + books_card + "\n" + res[last_endblock:]

open(p, "w", encoding="utf-8").write(res)
print("[FIXED] Inserted books card before final content endblock")

# 3. Remove helper scripts accidentally committed if present
for helper in ["fix_all.py", "fix_final.py", "fix_resources_books.py", "deploy_diag.py", "force_redeploy.py"]:
    if os.path.exists(helper):
        os.remove(helper)
        print(f"[CLEANUP] Removed helper script: {helper}")

# 4. Template syntax check
print("\n=== TEMPLATE SYNTAX CHECK ===")
try:
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("backend/templates"))
    errs = 0
    for root, dirs, files in os.walk("backend/templates"):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), "backend/templates").replace("\\", "/")
                try:
                    env.get_template(rel)
                except Exception as e:
                    errs += 1
                    print(f"[TEMPLATE ERROR] {rel}: {e}")
    if errs:
        raise SystemExit(1)
    print("All templates parse clean")
except ImportError:
    print("jinja2 unavailable locally; skipping syntax check")

# 5. Verify local markers
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
res = open("backend/templates/resources.html", encoding="utf-8").read()
article = open("backend/templates/learn/article.html", encoding="utf-8").read()
home = open("backend/templates/index.html", encoding="utf-8").read()

print("\n=== LOCAL VERIFY ===")
print("learn canonical block:", "{% block canonical" in learn)
print("learn OG/Twitter:", "og:image" in learn and "twitter:title" in learn)
print("resources canonical block:", "{% block canonical" in res)
print("resources OG/Twitter:", "og:image" in res and "twitter:title" in res)
print("resources See All Books:", "See All Books" in res)
print("resources book loop gone:", "{% for b in books" not in res)
print("article no trailing slash canonical:", "{{ base_url }}/learn/{{ article.slug }}{% endblock %}" in article)
print("home pricing:", "Pro - 499" in home and "Premium - 999" in home)
print("home no Cancel anytime:", "Cancel anytime" not in home)

# 6. Commit + push
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: place resources books card inside content and clean helper scripts"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())

r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")

# 7. Show latest commits
print("\n=== LATEST COMMITS ===")
print(subprocess.run(["git", "log", "--oneline", "-4"], capture_output=True, text=True).stdout)
