import subprocess, json, os

# === 1. BUILD /books PAGE ===
books_html = """{% extends "base.html" %}
{% block title %}Books & Playbooks | GRCWithGaurav{% endblock %}
{% block description %}Practical GRC and cybersecurity career playbooks by Gaurav Malhotra - interview guides, roadmaps, and frameworks you can use immediately.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/books{% endblock %}
{% block head %}
<meta property="og:title" content="Books & Playbooks | GRCWithGaurav">
<meta property="og:description" content="Practical GRC and cybersecurity career playbooks by Gaurav Malhotra - interview guides, roadmaps, and frameworks you can use immediately.">
<meta property="og:image" content="https://grcwithgaurav.com/static/og-default.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://grcwithgaurav.com/books">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Books & Playbooks | GRCWithGaurav">
<meta name="twitter:description" content="Practical GRC and cybersecurity career playbooks by Gaurav Malhotra.">
<meta name="twitter:image" content="https://grcwithgaurav.com/static/og-default.jpg">
{% endblock %}
{% block content %}
<div style="max-width:900px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Playbooks, not just theory.</h1>
 <p style="color:var(--muted);font-size:1.1rem;line-height:1.6;max-width:700px">Everything I've learned about breaking into GRC and cybersecurity, written down so you don't have to learn it the hard way.</p>

 <div style="display:grid;gap:1.5rem;margin-top:2.5rem">
  {% for b in books %}
  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">{{ b.title }}</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">{{ b.desc }}</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">{{ b.price }}</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra</span>
   </p>
   <a href="{{ b.link }}" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>
  {% endfor %}
 </div>

 <div class="card" style="padding:2rem;margin-top:2.5rem;text-align:center;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <h2 style="color:#fff;margin-top:0">Better together: CyberVerse AI + the playbooks</h2>
  <p style="color:var(--muted);max-width:600px;margin:0 auto 1rem">Upgrade to CyberVerse AI Pro this month and get any book free.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Upgrade & Claim Your Free Book &rarr;</a>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:2rem;text-align:center;background:#111;border:1px solid #222">
  <p style="color:var(--muted);margin:0">All books come with Gumroad's standard refund policy. If it's not useful to you, you get your money back — no hard feelings.</p>
 </div>
</div>
{% endblock %}
"""

with open("backend/templates/books.html", "w", encoding="utf-8") as f:
    f.write(books_html)
print("[CREATED] books.html")

# === 2. UPDATE site_routes.py: remove /books redirect, add /books route ===
sr = "backend/routers/site_routes.py"
c = open(sr, encoding="utf-8").read()

# Remove /books from redirect map
old_redirects = '_REDIRECTS = {"/books": "/resources", "/consulting": "/b2b", "/blog": "/learn", "/home": "/", "/about-us": "/about"}'
new_redirects = '_REDIRECTS = {"/consulting": "/b2b", "/blog": "/learn", "/home": "/", "/about-us": "/about"}'
if old_redirects in c:
    c = c.replace(old_redirects, new_redirects, 1)
    print("[UPDATED] removed /books from 301 redirects")

# Add /books route - insert before sitemap
books_route = '''

@router.get("/books", response_class=HTMLResponse)
async def books_page(request: Request):
    import json, os
    books_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "books.json")
    try:
        with open(books_path, encoding="utf-8") as f:
            books = json.load(f)
    except Exception:
        books = []
    return templates.TemplateResponse("books.html", {"request": request, "books": books})

'''

# Insert before sitemap
sitemap_idx = c.find('@router.get("/sitemap.xml")')
if sitemap_idx > 0 and "@router.get(\"/books\"" not in c:
    c = c[:sitemap_idx] + books_route + c[sitemap_idx:]
    print("[ADDED] /books route")

# Add /books to sitemap
old_paths = '    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b", "/careers", "/faq"] + TOOL_PATHS'
new_paths = '    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b", "/careers", "/faq", "/books"] + TOOL_PATHS'
if old_paths in c:
    c = c.replace(old_paths, new_paths, 1)
    print("[UPDATED] sitemap + /books")

open(sr, "w", encoding="utf-8").write(c)

# === 3. ADD /books TO NAV + FOOTER ===
base_html = "backend/templates/base.html"
c = open(base_html, encoding="utf-8").read()

# Nav: insert before CyberVerse AI CTA
old_nav = '<a href="/app.html" class="nav-cta">CyberVerse AI</a>'
new_nav = '<a href="/books">Books</a>\n            <a href="/app.html" class="nav-cta">CyberVerse AI</a>'
if old_nav in c and '>Books<' not in c:
    c = c.replace(old_nav, new_nav, 1)
    print("[UPDATED] nav: added Books link")

# Footer: add Books link
old_footer_link = '<a href="/about">About</a>'
new_footer_link = '<a href="/about">About</a>\n            <a href="/books">Books</a>'
if old_footer_link in c and '>Books</a>' not in c:
    c = c.replace(old_footer_link, new_footer_link, 1)
    print("[UPDATED] footer: added Books link")

open(base_html, "w", encoding="utf-8").write(c)

# === 4. PRICING TABLE ON HOMEPAGE CyberVerse Section ===
idx_html = "backend/templates/index.html"
c = open(idx_html, encoding="utf-8").read()

pricing_section = '''<section class="section">
    <h2>CyberVerse AI: Your Personal Mentor</h2>
    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Stop guessing. Start getting hired.</h3>
        <p>AI mock interviews, automated resume rewrites, and 6-month SOC/GRC roadmaps tailored to your exact skill gaps.</p>
        <a href="/app.html" class="btn-primary" style="display:inline-block; margin-top:1rem;">Launch CyberVerse AI</a>
    </div>
    <p style="text-align:center;color:var(--muted);font-style:italic;margin-top:1.2rem;font-size:.92rem">"The mock interviews exposed gaps I didn't know I had. Landed a SOC analyst role 3 weeks later." - Priya S., SOC Analyst</p>

    <div style="max-width:900px;margin:2.5rem auto 0;padding:2rem;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);border-radius:16px">
        <h3 style="color:#fff;text-align:center;margin-top:0">Start free. Upgrade when you're ready to go all in.</h3>
        <p style="text-align:center;color:var(--muted);margin-bottom:1.5rem">CyberVerse AI gives you real mock interviews with AI feedback — no credit card needed to start.</p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:750px;margin:0 auto">
            <div style="padding:1.5rem;background:#0a0a0a;border:1px solid #333;border-radius:12px">
                <h4 style="color:#fff;margin-top:0">Free</h4>
                <p style="color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem">Get started, no card needed</p>
                <ul style="color:#c9c9c9;font-size:.9rem;line-height:1.8;padding-left:1.2rem;margin:0">
                    <li>3 mock interviews / month</li>
                    <li>Basic feedback (pass/fail + summary)</li>
                    <li>GRC &amp; SOC fundamentals</li>
                </ul>
                <a href="/app.html" class="btn-secondary" style="display:block;text-align:center;margin-top:1.5rem">Start Free</a>
            </div>
            <div style="padding:1.5rem;background:#0a0a0a;border:2px solid var(--accent);border-radius:12px;position:relative">
                <span style="position:absolute;top:-12px;right:16px;background:var(--accent);color:#000;font-size:.75rem;font-weight:700;padding:.2rem .7rem;border-radius:10px">MOST POPULAR</span>
                <h4 style="color:var(--accent);margin-top:0">Pro</h4>
                <p style="color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem">For serious career builders</p>
                <ul style="color:#c9c9c9;font-size:.9rem;line-height:1.8;padding-left:1.2rem;margin:0">
                    <li>Unlimited interviews</li>
                    <li>Detailed scoring + improvement plan per answer</li>
                    <li>All topic tracks (Auditor, Analyst, Compliance)</li>
                    <li>Streak tracking + weak-area analytics</li>
                    <li>Shareable verified certificate</li>
                    <li>Priority AI response speed</li>
                </ul>
                <a href="/app.html" class="btn-primary" style="display:block;text-align:center;margin-top:1.5rem">Upgrade to Pro &rarr;</a>
                <p style="text-align:center;color:var(--muted);font-size:.75rem;margin-top:.6rem;margin-bottom:0">7-day money-back guarantee. Cancel anytime.</p>
            </div>
        </div>
    </div>
</section>'''

old_cv_section = '''<section class="section">
    <h2>CyberVerse AI: Your Personal Mentor</h2>
    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Stop guessing. Start getting hired.</h3>
        <p>AI mock interviews, automated resume rewrites, and 6-month SOC/GRC roadmaps tailored to your exact skill gaps.</p>
        <a href="/app.html" class="btn-primary" style="display:inline-block; margin-top:1rem;">Launch CyberVerse AI</a>
    </div>
    <p style="text-align:center;color:var(--muted);font-style:italic;margin-top:1.2rem;font-size:.92rem">"The mock interviews exposed gaps I didn't know I had. Landed a SOC analyst role 3 weeks later." - Priya S., SOC Analyst</p>
</section>'''

if old_cv_section in c:
    c = c.replace(old_cv_section, pricing_section, 1)
    open(idx_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] index.html - CyberVerse section replaced with pricing table")
else:
    print("[WARN] CyberVerse section pattern not matched")

# === 5. IN-ARTICLE UPSELL BOXES ===
# Inject book upsell box into article.body HTML for relevant articles
articles_py = "backend/content/articles.py"
c = open(articles_py, encoding="utf-8").read()

# Map of article slugs -> book recommendation
upsell_map = {
    'what-is-iso-27001': ('Breaking Into GRC', 'The exact interview questions and answers that got me and my students hired into GRC roles.', 'breaking-into-grc'),
    'grc-analyst-career-roadmap': ('Breaking Into GRC', 'A career-changer\'s guide to breaking into GRC — no coding, no IT degree required.', 'breaking-into-grc'),
    'how-to-start-grc-career': ('Breaking Into GRC', 'Everything I wish someone had told me before my first GRC interview.', 'breaking-into-grc'),
    'grc-interview-questions': ('Breaking Into GRC', '50+ real GRC interview questions with model answers, so you walk in prepared.', 'breaking-into-grc'),
    'soc-analyst-interview-questions': ('Breaking Into GRC', 'GRC and SOC interview frameworks that actually get offers, not just certificates.', 'breaking-into-grc'),
    'what-does-soc-analyst-do': ('Breaking Into GRC', 'The SOC-to-GRC career pivot playbook — and how to pick the right path.', 'breaking-into-grc'),
    'best-cybersecurity-certifications-beginners-2026': ('AI Workflows for Cybersecurity Professionals', 'Which certs actually pay off — and how to use AI to study 10x faster.', 'ai-workflows'),
    'cybersecurity-portfolio-guide': ('AI Workflows for Cybersecurity Professionals', 'AI workflows for building portfolio pieces that hiring managers actually notice.', 'ai-workflows'),
    'cybersecurity-salary-india-2026': ('AI Workflows for Cybersecurity Professionals', 'Real salary data + how AI-skilled security pros earn 30-40% more.', 'ai-workflows'),
    'splunk-vs-elastic-vs-sentinel': ('AI Workflows for Cybersecurity Professionals', 'Practitioner playbook: human-in-the-loop AI workflows for SIEM triage and threat intel.', 'ai-workflows'),
    'nist-csf-vs-iso-27001-vs-soc2': ('The AI Governance Playbook', 'Frameworks for governing AI itself — the emerging specialty paying $200K+.', 'ai-governance'),
    'vendor-risk-assessment-guide': ('The AI Governance Playbook', 'NIST AI RMF mapping + done-for-you AI risk assessment templates.', 'ai-governance'),
    'what-is-grc': ('Breaking Into GRC', 'Your complete GRC foundation — from frameworks to your first interview.', 'breaking-into-grc'),
    'iso-27001-risk-assessment': ('Breaking Into GRC', 'Risk assessment frameworks translated into career capital.', 'breaking-into-grc'),
}

upsell_html_template = '''<div style="margin:2rem 0;padding:1.5rem;border-radius:12px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
<p style="color:var(--accent);font-size:.85rem;font-weight:600;margin:0 0 .4rem;text-transform:uppercase;letter-spacing:.5px">Want the complete playbook?</p>
<h4 style="color:#fff;margin:.2rem 0 .5rem;font-size:1.2rem">{title}</h4>
<p style="color:#c9c9c9;margin:0 0 1rem;line-height:1.6">{hook}</p>
<a href="/books" style="display:inline-block;padding:.5rem 1.2rem;background:var(--accent);color:#000;border-radius:8px;font-weight:700;text-decoration:none;font-size:.9rem">Get the Guide &rarr;</a>
</div>
'''

import re
count = 0
for slug, (title, hook, _) in upsell_map.items():
    # Find article and inject upsell into body after 2nd h2
    pattern = f"'slug': '{slug}',"
    if pattern in c:
        # Find the body field for this article
        body_start = c.find("'body':", c.find(pattern))
        if body_start > 0:
            # Find end of body (next '}' at start of line or next article)
            body_end = c.find("}\n)", body_start)
            if body_end > 0:
                body_content = c[body_start:body_end]
                # Count h2 tags
                h2_count = body_content.lower().count("<h2")
                if h2_count >= 2:
                    # Find 2nd h2
                    first_h2 = body_content.lower().find("<h2")
                    second_h2 = body_content.lower().find("<h2", first_h2 + 3)
                    if second_h2 > 0:
                        # Find end of that h2 section (next </h2> + following content)
                        h2_end = body_content.find("</h2>", second_h2)
                        if h2_end > 0:
                            h2_end += 5  # include </h2>
                            upsell = upsell_html_template.format(title=title, hook=hook)
                            new_body = body_content[:h2_end] + upsell + body_content[h2_end:]
                            c = c[:body_start] + new_body + c[body_end:]
                            count += 1

print(f"[INJECTED] upsell boxes into {count} article bodies")

# Verify compile
try:
    compile(c, articles_py, "exec")
    print("[COMPILE] articles.py verified clean")
except SyntaxError as e:
    print(f"[ABORT] Syntax error: {e}")
    raise SystemExit(1)

open(articles_py, "w", encoding="utf-8").write(c)

# === 6. COMMIT + PUSH ===
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Monetization stage 1: /books page, pricing table, nav/footer links, article upsells"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
