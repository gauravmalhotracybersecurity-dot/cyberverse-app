import subprocess

# === 1. ADD upsell_book FIELD TO ARTICLES ===
ap = "backend/content/articles.py"
c = open(ap, encoding="utf-8").read()

upsell_map = {
    'what-is-iso-27001': {'title': 'Breaking Into GRC', 'hook': 'The exact interview questions and answers that got me and my students hired into GRC roles.'},
    'iso-27001-risk-assessment': {'title': 'Breaking Into GRC', 'hook': 'Risk assessment frameworks translated into career capital.'},
    'what-is-grc': {'title': 'Breaking Into GRC', 'hook': 'Your complete GRC foundation - from frameworks to your first interview.'},
    'grc-analyst-career-roadmap': {'title': 'Breaking Into GRC', 'hook': 'A career-changer\'s guide to breaking into GRC - no coding, no IT degree required.'},
    'grc-interview-questions': {'title': 'Breaking Into GRC', 'hook': '50+ real GRC interview questions with model answers, so you walk in prepared.'},
    'how-to-start-grc-career': {'title': 'Breaking Into GRC', 'hook': 'Everything I wish someone had told me before my first GRC interview.'},
    'what-does-soc-analyst-do': {'title': 'Breaking Into GRC', 'hook': 'The SOC-to-GRC career pivot playbook - and how to pick the right path.'},
    'soc-analyst-interview-questions': {'title': 'Breaking Into GRC', 'hook': 'GRC and SOC interview frameworks that actually get offers, not just certificates.'},
    'cybersecurity-salary-india-2026': {'title': 'AI Workflows for Cybersecurity Professionals', 'hook': 'Real salary data + how AI-skilled security pros earn 30-40% more.'},
    'best-cybersecurity-certifications-beginners-2026': {'title': 'AI Workflows for Cybersecurity Professionals', 'hook': 'Which certs actually pay off - and how to use AI to study 10x faster.'},
    'cybersecurity-portfolio-guide': {'title': 'AI Workflows for Cybersecurity Professionals', 'hook': 'AI workflows for building portfolio pieces that hiring managers actually notice.'},
    'splunk-vs-elastic-vs-sentinel': {'title': 'AI Workflows for Cybersecurity Professionals', 'hook': 'Practitioner playbook: human-in-the-loop AI workflows for SIEM triage and threat intel.'},
    'nist-csf-vs-iso-27001-vs-soc2': {'title': 'The AI Governance Playbook', 'hook': 'Frameworks for governing AI itself - the emerging specialty paying $200K+.'},
    'vendor-risk-assessment-guide': {'title': 'The AI Governance Playbook', 'hook': 'NIST AI RMF mapping + done-for-you AI risk assessment templates.'},
}

count = 0
for slug, upsell in upsell_map.items():
    pattern = f"'slug': '{slug}',"
    if pattern in c and "'upsell_book'" not in c[c.find(pattern):c.find(pattern)+2000]:
        # Find the closing }) for this article
        start = c.find(pattern)
        end = c.find("})", start)
        if end > start:
            upsell_field = f",\n    'upsell_book': {{'title': '{upsell['title']}', 'hook': '{upsell['hook']}'}}"
            c = c[:end] + upsell_field + c[end:]
            count += 1

print(f"[ADDED] upsell_book field to {count} articles")

# Verify
if "'upsell_book'" in c:
    print("[VERIFY] ✅ upsell_book field is in articles.py")
else:
    print("[VERIFY] ❌ upsell_book field injection FAILED")
    raise SystemExit(1)

open(ap, "w", encoding="utf-8").write(c)

# === 2. UPDATE article.html TEMPLATE ===
art_html = "backend/templates/learn/article.html"
c = open(art_html, encoding="utf-8").read()

upsell_template = """
 {% if article.upsell_book %}
 <div style="margin:2rem 0;padding:1.5rem;border-radius:12px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <p style="color:var(--accent);font-size:.85rem;font-weight:600;margin:0 0 .4rem;text-transform:uppercase;letter-spacing:.5px">Want the complete playbook?</p>
  <h4 style="color:#fff;margin:.2rem 0 .5rem;font-size:1.2rem">{{ article.upsell_book.title }}</h4>
  <p style="color:#c9c9c9;margin:0 0 1rem;line-height:1.6">{{ article.upsell_book.hook }}</p>
  <a href="/books" style="display:inline-block;padding:.5rem 1.2rem;background:var(--accent);color:#000;border-radius:8px;font-weight:700;text-decoration:none;font-size:.9rem">Get the Guide &rarr;</a>
 </div>
 {% endif %}
"""

if "article.body | safe" in c and "article.upsell_book" not in c:
    lines = c.split("\n")
    for i, line in enumerate(lines):
        if "article.body | safe" in line:
            lines.insert(i+1, upsell_template)
            break
    c = "\n".join(lines)
    open(art_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] article.html - upsell box rendering added")
    print("[VERIFY] ✅ Template rendering is in article.html")
else:
    print("[SKIP] upsell rendering already present or body not found")

# === 3. COMMIT + PUSH ===
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Monetization: add upsell_book field + template rendering"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
