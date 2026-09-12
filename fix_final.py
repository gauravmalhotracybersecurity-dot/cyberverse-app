import subprocess, urllib.request

# === 1. DIAGNOSE CURRENT LOCAL STATE ===
print("=== LOCAL FILE STATE ===")
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
res = open("backend/templates/resources.html", encoding="utf-8").read()

learn_has_canonical = "{% block canonical" in learn
learn_has_head = "{% block head" in learn
res_has_canonical = "{% block canonical" in res
res_has_head = "{% block head" in res
res_has_books_link = "See All Books" in res
res_has_book_loop = "{% for b in books" in res

print(f"  /learn canonical block: {learn_has_canonical}")
print(f"  /learn head block: {learn_has_head}")
print(f"  /resources canonical block: {res_has_canonical}")
print(f"  /resources head block: {res_has_head}")
print(f"  /resources 'See All Books': {res_has_books_link}")
print(f"  /resources book loop: {res_has_book_loop}")

# === 2. FIX /learn template ===
if not (learn_has_canonical and learn_has_head):
    title_idx = learn.find("{% block title %}")
    if title_idx > 0:
        end_title = learn.find("{% endblock %}", title_idx) + 14
        meta_block = """
{% block canonical %}https://grcwithgaurav.com/learn{% endblock %}
{% block head %}
<meta property="og:image" content="https://grcwithgaurav.com/static/og-default.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://grcwithgaurav.com/learn">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://grcwithgaurav.com/static/og-default.jpg">
<meta name="twitter:title" content="Learn Cybersecurity, GRC & ISO 27001 | GRCWithGaurav">
<meta name="twitter:description" content="Practical, human-reviewed guides on ISO 27001, GRC, SOC careers and AI in cybersecurity - each linked to free tools and CyberVerse AI.">
{% endblock %}
"""
        learn = learn[:end_title] + meta_block + learn[end_title:]
        open("backend/templates/learn/index.html", "w", encoding="utf-8").write(learn)
        print("\n[FIX] /learn: added canonical + head blocks")
else:
    print("\n[SKIP] /learn already has blocks")

# === 3. FIX /resources template (canonical + head + books card) ===
res_changed = False
if not (res_has_canonical and res_has_head):
    title_idx = res.find("{% block title %}")
    if title_idx > 0:
        end_title = res.find("{% endblock %}", title_idx) + 14
        meta_block = """
{% block canonical %}https://grcwithgaurav.com/resources{% endblock %}
{% block head %}
<meta property="og:image" content="https://grcwithgaurav.com/static/og-default.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://grcwithgaurav.com/resources">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://grcwithgaurav.com/static/og-default.jpg">
<meta name="twitter:title" content="Free Cybersecurity Resources & Starter Kit | GRCWithGaurav">
<meta name="twitter:description" content="Free cybersecurity starter kit: ISO 27001 risk register, audit checklist, GRC interview questions, career roadmap and resume template - plus ebooks.">
{% endblock %}
"""
        res = res[:end_title] + meta_block + res[end_title:]
        res_changed = True
        print("[FIX] /resources: added canonical + head blocks")

if "See All Books" not in res:
    endblock_idx = res.find("{% endblock %}")
    if endblock_idx > 0:
        books_card = """
<div class="card" style="padding:1.5rem;margin-top:1.5rem">
 <h3 style="margin-top:0">Ebooks & Playbooks</h3>
 <p style="color:var(--muted);margin:.5rem 0 1rem">Three practical playbooks for GRC and AI in security careers.</p>
 <a href="/books" class="btn-primary" style="display:inline-block">See All Books &rarr;</a>
</div>
"""
        res = res[:endblock_idx] + books_card + res[endblock_idx:]
        res_changed = True
        print("[FIX] /resources: added books card")

if res_changed:
    open("backend/templates/resources.html", "w", encoding="utf-8").write(res)

# === 4. VERIFY LOCAL STATE ===
print("\n=== POST-FIX LOCAL STATE ===")
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
res = open("backend/templates/resources.html", encoding="utf-8").read()
print(f"  /learn canonical: {'{% block canonical' in learn}")
print(f"  /learn head: {'{% block head' in learn}")
print(f"  /resources canonical: {'{% block canonical' in res}")
print(f"  /resources head: {'{% block head' in res}")
print(f"  /resources 'See All Books': {'See All Books' in res}")

# === 5. COMMIT + PUSH + MANUAL DEPLOY REMINDER ===
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: /learn + /resources canonical/meta blocks + books card"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")

# === 6. IMMEDIATELY TRIGGER MANUAL DEPLOY VIA EMPTY COMMIT (belt + suspenders) ===
r = subprocess.run(["git", "commit", "--allow-empty", "-m", "Trigger manual Render deploy"], capture_output=True, text=True)
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[TRIGGER] empty commit pushed to wake Render")
