import subprocess, re

# === 1. SURGICALLY REMOVE ALL INJECTED upsell_book FRAGMENTS ===
ap = "backend/content/articles.py"
c = open(ap, encoding="utf-8").read()
before = c.count("'upsell_book'")
pat = re.compile(r",?\n    'upsell_book': \{'title': '.+?', 'hook': '.+?'\},?")
c, n = pat.subn("", c)
print(f"[REMOVED] {n} injected upsell_book fragments (had {before} occurrences)")
open(ap, "w", encoding="utf-8").write(c)

# Compile + import check
try:
    compile(c, ap, "exec")
    print("[COMPILE] articles.py clean")
except SyntaxError as e:
    print(f"[STILL BROKEN] {e}")
    raise SystemExit(1)

r = subprocess.run(["backend/venv/Scripts/python.exe", "-c",
    "import sys; sys.path.insert(0,'backend'); from content import articles; print(len(articles.ARTICLES)); print([a['slug'] for a in articles.ARTICLES][:5])"],
    capture_output=True, text=True)
print(f"[IMPORT] {r.stdout.strip() or r.stderr.strip()}")

# === 2. CLEAN article.html + ADD TEMPLATE-ONLY UPSELL (no articles.py edits ever again) ===
ah = "backend/templates/learn/article.html"
t = open(ah, encoding="utf-8").read()

# Remove any old broken upsell block
t = re.sub(r"\{% if article\.upsell_book %\}.*?\{% endif %\}", "", t, flags=re.DOTALL)

if "set upsells" not in t:
    block = '''{% set upsells = {
 'what-is-iso-27001': ("Breaking Into GRC", "The exact interview questions and answers that got me and my students hired into GRC roles."),
 'iso-27001-risk-assessment': ("Breaking Into GRC", "Risk assessment frameworks translated into career capital."),
 'what-is-grc': ("Breaking Into GRC", "Your complete GRC foundation - from frameworks to your first interview."),
 'grc-analyst-career-roadmap': ("Breaking Into GRC", "A career-changer's guide to breaking into GRC - no coding, no IT degree required."),
 'grc-interview-questions': ("Breaking Into GRC", "50+ real GRC interview questions with model answers, so you walk in prepared."),
 'how-to-start-grc-career': ("Breaking Into GRC", "Everything I wish someone had told me before my first GRC interview."),
 'what-does-soc-analyst-do': ("Breaking Into GRC", "The SOC-to-GRC career pivot playbook - and how to pick the right path."),
 'soc-analyst-interview-questions': ("Breaking Into GRC", "GRC and SOC interview frameworks that actually get offers, not just certificates."),
 'cybersecurity-salary-india-2026': ("AI Workflows for Cybersecurity Professionals", "Real salary data + how AI-skilled security pros earn 30-40% more."),
 'best-cybersecurity-certifications-beginners-2026': ("AI Workflows for Cybersecurity Professionals", "Which certs actually pay off - and how to use AI to study 10x faster."),
 'cybersecurity-portfolio-guide': ("AI Workflows for Cybersecurity Professionals", "AI workflows for building portfolio pieces that hiring managers actually notice."),
 'splunk-vs-elastic-vs-sentinel': ("AI Workflows for Cybersecurity Professionals", "Practitioner playbook: human-in-the-loop AI workflows for SIEM triage and threat intel."),
 'nist-csf-vs-iso-27001-vs-soc2': ("The AI Governance Playbook", "Frameworks for governing AI itself - the emerging specialty paying $200K+."),
 'vendor-risk-assessment-guide': ("The AI Governance Playbook", "NIST AI RMF mapping + done-for-you AI risk assessment templates.")
} %}
{% if article.slug in upsells %}
 <div style="margin:2rem 0;padding:1.5rem;border-radius:12px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <p style="color:var(--accent);font-size:.85rem;font-weight:600;margin:0 0 .4rem;text-transform:uppercase;letter-spacing:.5px">Want the complete playbook?</p>
  <h4 style="color:#fff;margin:.2rem 0 .5rem;font-size:1.2rem">{{ upsells[article.slug][0] }}</h4>
  <p style="color:#c9c9c9;margin:0 0 1rem;line-height:1.6">{{ upsells[article.slug][1] }}</p>
  <a href="/books" style="display:inline-block;padding:.5rem 1.2rem;background:var(--accent);color:#000;border-radius:8px;font-weight:700;text-decoration:none;font-size:.9rem">Get the Guide &rarr;</a>
 </div>
{% endif %}'''
    lines = t.split("\n")
    for i, line in enumerate(lines):
        if "article.body | safe" in line:
            lines.insert(i+1, block)
            break
    t = "\n".join(lines)
    print("[UPDATED] article.html - template-only upsell mapping added")

open(ah, "w", encoding="utf-8").write(t)

# === 3. COMMIT + PUSH ===
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: restore articles.py integrity + template-only upsell mapping"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
