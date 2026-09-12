import subprocess, re

p = "backend/templates/resources.html"
c = open(p, encoding="utf-8").read()
print("=== BEFORE ===")
print(f"  length: {len(c)}")
print(f"  stray card occurrences: {len(re.findall(r'Ebooks (?:&|&amp;) Playbooks', c))}")

# 1. Remove ALL injected ebook cards wherever they are
pat = re.compile(r'<div class="card"[^>]*>\s*<h3[^>]*>Ebooks (?:&|&amp;) Playbooks</h3>.*?</div>\s*', re.DOTALL)
c, n = pat.subn("", c)
print(f"  removed: {n} card block(s)")

# 2. Remove leftover '">' artifact lines
c = re.sub(r'\n[ \t]*"[ \t]*>[ \t]*\n', '\n', c)

# 3. Show head blocks to confirm they are clean now
for b in ["title", "description", "canonical"]:
    i = c.find("{% block " + b)
    if i >= 0:
        seg = c[i:i+250].split("{% endblock %}")[0]
        print(f"\n  --- block {b} ---")
        print("  " + seg[:180].replace("\n", " | "))

# 4. Insert ONE clean card at the END of the content block
card = ''' <div class="card" style="padding:1.5rem;margin-top:1.5rem">
  <h3 style="margin-top:0">Ebooks &amp; Playbooks</h3>
  <p style="color:var(--muted);margin:.5rem 0 1rem">Three practical playbooks for GRC and AI in security careers.</p>
  <a href="/books" class="btn-primary" style="display:inline-block">See All Books &rarr;</a>
 </div>
'''
content_idx = c.find("{% block content %}")
last_end = c.rfind("{% endblock %}")
if content_idx < 0 or last_end < content_idx:
    print("[ERROR] block structure unexpected - aborting")
    raise SystemExit(1)
c = c[:last_end] + card + c[last_end:]
open(p, "w", encoding="utf-8").write(c)

# 5. Verify structure
c2 = open(p, encoding="utf-8").read()
cards = len(re.findall(r'Ebooks (?:&|&amp;) Playbooks', c2))
inside_content = c2.find("Ebooks") > c2.find("{% block content %}")
print(f"\n=== AFTER ===")
print(f"  cards: {cards} (must be 1)")
print(f"  card inside content block: {inside_content} (must be True)")

# 6. Jinja parse check
try:
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("backend/templates"))
    env.get_template("resources.html")
    print("  jinja parse: OK")
except Exception as e:
    print(f"  [TEMPLATE ERROR] {e}")
    raise SystemExit(1)

# 7. Commit + push
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: resources page - remove stray head-injected cards, single clean books card in content"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
