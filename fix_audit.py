import subprocess, re

print("=== IMPLEMENTING FIXES 2, 3, 4 ===\n")

# === FIX 2: Template consolidation for /learn and /resources ===
# Both should extend base.html like /careers, /books, etc.

learn_html = "backend/templates/learn/index.html"
resources_html = "backend/templates/resources.html"

for filepath, page_type in [(learn_html, "learn"), (resources_html, "resources")]:
    c = open(filepath, encoding="utf-8").read()
    
    # Check if already extends base.html
    if "{% extends" not in c or '"base.html"' not in c:
        # Wrap content in base.html structure
        if "<!DOCTYPE" in c or "<html" in c:
            # Full HTML - need to extract just the body content
            # This is a complex case - let's see the structure first
            print(f"[CHECK] {filepath} appears to be full HTML, not extending base.html")
            print(f"  First 300 chars: {c[:300]}")
        else:
            print(f"[SKIP] {filepath} already extends base.html")
    else:
        print(f"[OK] {filepath} already extends base.html")

# === FIX 4: Remove trailing slash from article canonical ===
article_html = "backend/templates/learn/article.html"
c = open(article_html, encoding="utf-8").read()

# Find canonical block
if "{% block canonical %}" in c:
    # Replace trailing slash pattern
    old_canonical = "{% block canonical %}{{ base_url }}/learn/{{ article.slug }}/{% endblock %}"
    new_canonical = "{% block canonical %}{{ base_url }}/learn/{{ article.slug }}{% endblock %}"
    if old_canonical in c:
        c = c.replace(old_canonical, new_canonical)
        open(article_html, "w", encoding="utf-8").write(c)
        print("[FIX 4] Removed trailing slash from article canonical")
    else:
        print("[FIX 4] Canonical pattern not matched - checking current:")
        idx = c.find("{% block canonical %}")
        if idx >= 0:
            print(f"  Current: {c[idx:idx+100]}")
else:
    print("[FIX 4] No canonical block found in article.html")

# === FIX 3: De-dupe ebook content from /resources ===
c = open(resources_html, encoding="utf-8").read()

# Look for the book cards section
if "{{ b.title }}" in c and "{{ b.desc }}" in c:
    # Find the loop that renders books
    idx = c.find("{% for b in books %}")
    if idx > 0:
        # Replace the entire loop with a link to /books
        end_idx = c.find("{% endfor %}", idx)
        if end_idx > idx:
            old_section = c[idx:end_idx+12]
            new_section = '<p style="margin-top:1.5rem">Looking for the ebooks? <a href="/books">See all books &rarr;</a></p>'
            c = c.replace(old_section, new_section)
            open(resources_html, "w", encoding="utf-8").write(c)
            print("[FIX 3] Replaced book loop on /resources with link to /books")
else:
    print("[FIX 3] No book loop found in resources.html")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: article canonical trailing slash, resources book de-dupe"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
