import subprocess

# ---------- /resources : remove BOTH book blocks, add free-identity line ----------
p = "backend/templates/resources.html"
c = open(p, encoding="utf-8").read()

# 1. Delete the leftover "Ebooks" H2 section (h2 ... {% endif %})
start = c.find('<h2 style="color:#fff;margin-top:3rem">Ebooks</h2>')
if start >= 0:
    end = c.find('{% endif %}', start)
    if end < 0:
        print("[ERROR] no endif after Ebooks h2")
        raise SystemExit(1)
    end += len('{% endif %}')
    c = c[:start] + c[end:]
    print("[REMOVED] leftover 'Ebooks' H2 section")
else:
    print("[SKIP] Ebooks H2 not found")

# 2. Replace the playbooks card with ONE thin dashed pointer strip
old_card = ''' <div class="card" style="padding:1.5rem;margin-top:1.5rem">
  <h3 style="margin-top:0">Ready for the full playbooks?</h3>
  <p style="color:var(--muted);margin:.5rem 0 1rem">Five practitioner playbooks and toolkits - $9 each, or all five for $35.</p>
  <a href="/books" class="btn-primary" style="display:inline-block">See All Books &rarr;</a>
 </div>'''
new_strip = ''' <div style="margin-top:3rem;padding:1rem 1.5rem;border:1px dashed #333;border-radius:12px;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap">
  <p style="margin:0;color:var(--muted);font-size:.92rem">Free templates got you started? The in-depth paid playbooks live on the Books page.</p>
  <a href="/books" style="color:var(--accent);font-weight:600;text-decoration:none;white-space:nowrap">Browse Books &rarr;</a>
 </div>'''
if old_card in c:
    c = c.replace(old_card, new_strip, 1)
    print("[REPLACED] playbooks card -> thin dashed pointer strip")
else:
    print("[SKIP] playbooks card pattern not found")

# 3. Free-identity line under H1
old_h1 = '<h1 style="color:#fff">Resources</h1>'
new_h1 = '<h1 style="color:#fff">Resources</h1>\n <p style="color:var(--accent);font-weight:700;margin:.5rem 0 0;font-size:.95rem">Everything on this page is free to generate &mdash; no payment, no account needed.</p>'
if old_h1 in c and 'Everything on this page is free' not in c:
    c = c.replace(old_h1, new_h1, 1)
    print("[ADDED] free-identity line under H1")

open(p, "w", encoding="utf-8").write(c)

# ---------- /books : commerce trust-line under H1 ----------
p = "backend/templates/books.html"
b = open(p, encoding="utf-8").read()
old_h1 = '<h1 style="color:#fff">Playbooks, not just theory.</h1>'
new_h1 = '<h1 style="color:#fff">Playbooks, not just theory.</h1>\n <p style="color:var(--muted);margin:.5rem 0 0;font-size:.95rem">Instant PDF download &middot; Gumroad checkout &middot; refund guarantee &middot; bundle saves $10</p>'
if old_h1 in b and 'Instant PDF download &middot;' not in b:
    b = b.replace(old_h1, new_h1, 1)
    open(p, "w", encoding="utf-8").write(b)
    print("[ADDED] commerce trust-line under /books H1")

# ---------- parse check + commit ----------
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("backend/templates"))
for t in ["resources.html", "books.html"]:
    try:
        env.get_template(t)
        print(f"{t}: parses OK")
    except Exception as e:
        print(f"{t}: BROKEN - {e}")
        raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "UX: /resources = pure free page (single thin books pointer); /books = commerce trust-line"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
