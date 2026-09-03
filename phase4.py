import os, subprocess

os.makedirs("backend/content", exist_ok=True)
os.makedirs("backend/templates/learn", exist_ok=True)
open("backend/content/__init__.py", "w", encoding="utf-8").write("")

# ================= 1. ARTICLE DATABASE (CMS) =================
articles = r'''
ARTICLES = [
    {
        "slug": "what-is-iso-27001",
        "title": "What is ISO 27001? The Complete Beginner Guide (2026)",
        "category": "ISO 27001",
        "description": "What ISO 27001 certifies, what changed in the 2022 revision, how Annex A is structured, how certification works, and how to start implementing this week.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "8 min read",
        "tools": [
            {"href": "/tools/iso-gap-assessment", "label": "ISO 27001 Gap Assessment"},
            {"href": "/tools/iso-risk-calculator", "label": "ISO 27001 Risk Calculator"},
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"}
        ],
        "related": [
            {"slug": "iso-27001-risk-assessment", "title": "ISO 27001 Risk Assessment Explained (With a Worked Example)"}
        ],
        "faq": [
            ["Is ISO 27001 mandatory?", "No. It is a voluntary international standard. However, enterprise contracts, tenders and sector regulations often make certification a practical requirement to win business, especially in SaaS, fintech and healthcare."],
            ["How long does ISO 27001 certification take?", "Most small to mid-size organizations take 3 to 12 months from kickoff to certificate, depending on scope, existing maturity and how much documentation already exists."],
            ["What is the difference between ISO 27001 and ISO 27002?", "ISO 27001 defines the requirements for the management system and is the standard you certify against. ISO 27002 is the companion code of practice explaining how to implement the Annex A controls."],
            ["Do I need a consultant to get certified?", "No, but experienced help shortens the timeline. You can self-implement using the standard, a gap assessment and a solid risk register - the free tools on this site produce the core artifacts."]
        ],
        "body": """
<p>ISO/IEC 27001 is the international standard for an <strong>Information Security Management System (ISMS)</strong>. It does not tell you which firewall to buy - it requires you to build a management system that identifies your information security risks and treats them consistently, with evidence an auditor can verify.</p>
<h2>What ISO 27001 actually certifies</h2>
<p>Certification covers your <strong>management system</strong>, not a product. An auditor checks that you defined a scope, obtained leadership commitment, assessed risks, selected controls, and that you monitor, audit and improve the system over time. That is why a 20-person SaaS company and a bank can both be certified - the standard scales with your risk.</p>
<h2>What changed in the 2022 revision</h2>
<ul>
<li>The standard was restructured and renamed <strong>ISO/IEC 27001:2022</strong>.</li>
<li>Annex A now contains <strong>93 controls in four themes</strong> instead of 114 in 14 domains.</li>
<li>11 new controls were added, including threat intelligence, cloud security, ICT readiness for business continuity, secure coding, and data masking.</li>
<li>Certificates against the old 2013 version had to transition - any certificate you see today should be 2022-based.</li>
</ul>
<h2>The structure: Clauses 4-10</h2>
<ul>
<li><strong>Clause 4 - Context:</strong> internal/external issues, interested parties, ISMS scope.</li>
<li><strong>Clause 5 - Leadership:</strong> management commitment, policy, roles.</li>
<li><strong>Clause 6 - Planning:</strong> risk assessment, risk treatment, Statement of Applicability (SoA), objectives.</li>
<li><strong>Clause 7 - Support:</strong> competence, awareness, documented information.</li>
<li><strong>Clause 8 - Operation:</strong> doing what you planned, including periodic risk assessments.</li>
<li><strong>Clause 9 - Performance evaluation:</strong> metrics, internal audit, management review.</li>
<li><strong>Clause 10 - Improvement:</strong> nonconformities and corrective action.</li>
</ul>
<h2>Annex A: 93 controls in four themes</h2>
<ul>
<li><strong>Organizational (37):</strong> policies, vendor relationships, incident management, business continuity.</li>
<li><strong>People (8):</strong> screening, terms of employment, awareness training.</li>
<li><strong>Physical (14):</strong> perimeters, entry controls, equipment protection.</li>
<li><strong>Technological (34):</strong> access control, cryptography, logging, secure development.</li>
</ul>
<h2>How certification works</h2>
<ol>
<li><strong>Stage 1 audit:</strong> the certification body reviews documentation and readiness.</li>
<li><strong>Stage 2 audit:</strong> the auditor checks the ISMS is actually implemented and effective.</li>
<li><strong>Surveillance audits:</strong> annual check-ins in years 1 and 2.</li>
<li><strong>Recertification:</strong> full audit at year 3, then the cycle repeats.</li>
</ol>
<h2>How to start implementing (this week)</h2>
<ol>
<li>Define scope and get a signed information security policy (Clauses 4-5).</li>
<li>Run a <a href="/tools/iso-gap-assessment">gap assessment</a> to see where you stand.</li>
<li>Perform a <a href="/tools/iso-risk-calculator">risk assessment</a> using a documented 5x5 method.</li>
<li>Export a <a href="/tools/risk-register-generator">risk register</a> with owners, treatments and target dates.</li>
<li>Use the register to build your Statement of Applicability, then schedule an internal audit.</li>
</ol>
<h2>Common beginner mistakes</h2>
<ul>
<li>Writing 80 policies before doing a single risk assessment (the standard is risk-driven, not document-driven).</li>
<li>Scoping too broadly - certify the part of the business clients care about first.</li>
<li>Treating the SoA as a checklist instead of a justified decision record.</li>
</ul>
"""
    },
    {
        "slug": "iso-27001-risk-assessment",
        "title": "ISO 27001 Risk Assessment Explained (With a Worked Example)",
        "category": "ISO 27001",
        "description": "Clause 6.1.2 requirements, a simple 5x5 likelihood-impact method, a worked example risk table, and the four treatment options - with free tools to produce your register.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "6 min read",
        "tools": [
            {"href": "/tools/iso-risk-calculator", "label": "ISO 27001 Risk Calculator"},
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"}
        ],
        "related": [
            {"slug": "what-is-iso-27001", "title": "What is ISO 27001? The Complete Beginner Guide (2026)"}
        ],
        "faq": [
            ["How often should an ISO 27001 risk assessment be repeated?", "At planned intervals - commonly annually - and whenever a significant change occurs, such as a new system, a major incident, a new vendor or a change in scope."],
            ["What is risk acceptance and who signs it?", "Risks above your acceptance level must be treated. Any risk deliberately left above it must be signed off by the risk owner, because acceptance is a business decision, not a technical one."]
        ],
        "body": """
<p>Risk assessment is the engine of ISO 27001. Clause 6.1.2 requires you to <strong>define a method</strong> - including risk criteria and an acceptance level - then identify, analyse and evaluate risks, and retain documented results. The standard does not force a formula; it forces consistency. Here is a method that passes audits and is simple enough to run today.</p>
<h2>A simple, auditable 5x5 method</h2>
<p>Score each risk as <strong>Likelihood (1-5) x Impact (1-5)</strong>, giving a 1-25 score. Define bands up front, for example: 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical. State your acceptance level (for example: accept nothing above Medium without sign-off). Documenting the method <em>before</em> scoring is what makes it auditable.</p>
<h2>Worked example</h2>
<table>
<tr><th>Asset</th><th>Threat / Vulnerability</th><th>L</th><th>I</th><th>Score</th><th>Level</th><th>Treatment</th></tr>
<tr><td>Customer database</td><td>Ransomware; unpatched OS, no admin MFA</td><td>4</td><td>5</td><td>20</td><td>Critical</td><td>Mitigate: EDR, MFA, offline backups</td></tr>
<tr><td>Employee laptops</td><td>Theft; no full-disk encryption</td><td>3</td><td>4</td><td>12</td><td>High</td><td>Mitigate: FDE + MDM remote wipe</td></tr>
<tr><td>SaaS admin console</td><td>Credential phishing; no phishing-resistant MFA</td><td>3</td><td>4</td><td>12</td><td>High</td><td>Mitigate: FIDO2 keys + awareness training</td></tr>
<tr><td>Marketing site</td><td>Defacement; outdated CMS plugins</td><td>2</td><td>2</td><td>4</td><td>Low</td><td>Accept with patch monitoring</td></tr>
</table>
<h2>The four treatment options</h2>
<ul>
<li><strong>Mitigate:</strong> apply controls (most common) - e.g., MFA, encryption, EDR.</li>
<li><strong>Transfer:</strong> shift impact, e.g., cyber insurance or a contractually responsible vendor.</li>
<li><strong>Avoid:</strong> stop the activity causing the risk.</li>
<li><strong>Accept:</strong> consciously live with it, with risk-owner sign-off.</li>
</ul>
<h2>From assessment to register to SoA</h2>
<p>Every assessed risk becomes a register row: asset, threat, vulnerability, score, existing controls, treatment, owner and target date - you can generate and export this with the <a href="/tools/risk-register-generator">Risk Register Generator</a>. The treatments you select then map to Annex A controls in your <strong>Statement of Applicability</strong>, closing the loop between Clauses 6 and 8. If you are new to the standard, start with the <a href="/learn/what-is-iso-27001">beginner guide</a> first.</p>
"""
    }
]
'''
open("backend/content/articles.py", "w", encoding="utf-8").write(articles.strip() + "\n")
print("[CREATED] content/articles.py (2 pillar articles)")

# ================= 2. LEARN INDEX TEMPLATE =================
learn_index = """{% extends "base.html" %}
{% block title %}Learn Cybersecurity, GRC & ISO 27001 | GRCWithGaurav{% endblock %}
{% block description %}Practical, human-reviewed guides on ISO 27001, GRC, SOC careers and AI in cybersecurity - each linked to free tools and CyberVerse AI.{% endblock %}
{% block content %}
<div style="max-width:1000px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Learn</h1>
 <p style="color:var(--muted);max-width:720px">Original, practical guides for security and GRC professionals. Every guide links to a free tool and to CyberVerse AI so you can turn reading into practice.</p>
 {% for cat, arts in categories.items() %}
 <h2 style="color:var(--accent);margin-top:2.5rem">{{ cat }}</h2>
 <div class="grid-3">
  {% for a in arts %}
  <div class="card"><h3 style="font-size:1.05rem">{{ a.title }}</h3><p style="font-size:.88rem">{{ a.description }}</p><p style="color:var(--muted);font-size:.78rem">{{ a.date }} &middot; {{ a.read }}</p><a href="/learn/{{ a.slug }}">Read &rarr;</a></div>
  {% endfor %}
 </div>
 {% endfor %}
 <div style="margin-top:3rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center">
  <h2 style="color:#fff;margin:0 0 .5rem">Reading is not practicing.</h2>
  <p style="color:var(--muted)">CyberVerse AI turns every concept above into mock interview questions and grades your answers out loud.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Practice with CyberVerse AI &rarr;</a>
 </div>
</div>
{% endblock %}"""
open("backend/templates/learn/index.html", "w", encoding="utf-8").write(learn_index)
print("[CREATED] learn/index.html")

# ================= 3. ARTICLE TEMPLATE (SEO + SCHEMA) =================
article_tpl = """{% extends "base.html" %}
{% block title %}{{ article.title }} | GRCWithGaurav{% endblock %}
{% block description %}{{ article.description }}{% endblock %}
{% block canonical %}{{ base_url }}/learn/{{ article.slug }}/{% endblock %}
{% block head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ article.title }}",
  "description": "{{ article.description }}",
  "datePublished": "{{ article.date }}",
  "author": { "@type": "Person", "name": "{{ article.author }}" },
  "publisher": { "@type": "Organization", "name": "GRCWithGaurav" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "{{ base_url }}/" },
    { "@type": "ListItem", "position": 2, "name": "Learn", "item": "{{ base_url }}/learn" },
    { "@type": "ListItem", "position": 3, "name": "{{ article.title }}" }
  ]
}
</script>
{% if article.faq %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {% for q, a in article.faq %}
    { "@type": "Question", "name": "{{ q }}", "acceptedAnswer": { "@type": "Answer", "text": "{{ a }}" } }{% if not loop.last %},{% endif %}
    {% endfor %}
  ]
}
</script>
{% endif %}
<style>
 .wrap{max-width:840px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 h1{color:#fff;line-height:1.25}
 .meta{color:var(--muted);font-size:.85rem;margin:.5rem 0 1.5rem}
 .prose h2{color:#fff;margin-top:2.2rem}
 .prose p,.prose li{color:#c9c9c9;line-height:1.75}
 .prose a{color:var(--accent)}
 .prose table{width:100%;border-collapse:collapse;font-size:.83rem;margin:1rem 0}
 .prose th,.prose td{border:1px solid #333;padding:.5rem;text-align:left;color:var(--text);vertical-align:top}
 .prose th{color:var(--accent)}
 details{background:#111;border:1px solid #222;border-radius:8px;padding:.7rem 1rem;margin:.5rem 0}
 summary{color:#fff;cursor:pointer;font-weight:600}
 details p{color:#c9c9c9;margin:.5rem 0 0}
 .side-box{margin-top:2.5rem;padding:1.4rem;border-radius:12px;background:#111;border:1px solid #222}
 .side-box h3{color:var(--accent);margin-top:0}
 .cta-card{margin-top:2rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/learn">Learn</a> / {{ article.title }}</div>
 <h1>{{ article.title }}</h1>
 <div class="meta">By {{ article.author }} &middot; {{ article.date }} &middot; {{ article.read }}</div>
 <div class="prose">{{ article.body | safe }}</div>

 {% if article.tools %}
 <div class="side-box">
  <h3>Free tools for this guide</h3>
  <p style="color:var(--muted);margin:0">{% for t in article.tools %}<a href="{{ t.href }}">{{ t.label }}</a>{% if not loop.last %} &middot; {% endif %}{% endfor %}</p>
 </div>
 {% endif %}

 {% if article.related %}
 <div class="side-box">
  <h3>Continue in this cluster</h3>
  <ul style="margin:0;padding-left:1.1rem">{% for r in article.related %}<li><a href="/learn/{{ r.slug }}">{{ r.title }}</a></li>{% endfor %}</ul>
 </div>
 {% endif %}

 {% if article.faq %}
 <h2 style="color:#fff;margin-top:2.5rem">Frequently asked questions</h2>
 {% for q, a in article.faq %}
 <details><summary>{{ q }}</summary><p>{{ a }}</p></details>
 {% endfor %}
 {% endif %}

 <div class="cta-card">
  <h2 style="color:#fff;margin:0 0 .5rem">Can you explain this in an interview?</h2>
  <p style="color:var(--muted)">CyberVerse AI asks you this topic out loud and grades your answer like a hiring manager.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Practice with CyberVerse AI &rarr;</a>
 </div>
</div>
{% endblock %}"""
open("backend/templates/learn/article.html", "w", encoding="utf-8").write(article_tpl)
print("[CREATED] learn/article.html (Article + Breadcrumb + FAQ schema)")

# ================= 4. FULL SITE ROUTES (incl. sitemap + robots) =================
routes = '''from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
import os
from content.articles import ARTICLES

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

# Flip to https://grcwithgaurav.com when the main domain DNS is migrated to Render
BASE_URL = "https://cyberverse.grcwithgaurav.com"

TOOL_PATHS = [
    "/tools/iso-risk-calculator",
    "/tools/cvss-calculator",
    "/tools/iso-gap-assessment",
    "/tools/ats-resume-checker",
    "/tools/risk-register-generator",
]

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/tools", response_class=HTMLResponse)
async def tools_index(request: Request):
    return templates.TemplateResponse("tools/index.html", {"request": request})

@router.get("/tools/iso-risk-calculator", response_class=HTMLResponse)
async def iso_risk_calculator(request: Request):
    return templates.TemplateResponse("tools/iso_risk_calculator.html", {"request": request})

@router.get("/tools/cvss-calculator", response_class=HTMLResponse)
async def cvss_calculator(request: Request):
    return templates.TemplateResponse("tools/cvss_calculator.html", {"request": request})

@router.get("/tools/iso-gap-assessment", response_class=HTMLResponse)
async def iso_gap_assessment(request: Request):
    return templates.TemplateResponse("tools/iso_gap_assessment.html", {"request": request})

@router.get("/tools/ats-resume-checker", response_class=HTMLResponse)
async def ats_resume_checker(request: Request):
    return templates.TemplateResponse("tools/ats_resume_checker.html", {"request": request})

@router.get("/tools/risk-register-generator", response_class=HTMLResponse)
async def risk_register_generator(request: Request):
    return templates.TemplateResponse("tools/risk_register_generator.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
async def learn_index(request: Request):
    cats = {}
    for a in ARTICLES:
        cats.setdefault(a["category"], []).append(a)
    return templates.TemplateResponse("learn/index.html", {"request": request, "categories": cats})

@router.get("/learn/{slug}", response_class=HTMLResponse)
async def learn_article(request: Request, slug: str):
    art = next((a for a in ARTICLES if a["slug"] == slug), None)
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse("learn/article.html", {"request": request, "article": art, "base_url": BASE_URL})

@router.get("/careers", response_class=HTMLResponse)
@router.get("/resources", response_class=HTMLResponse)
async def placeholders(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/sitemap.xml")
async def sitemap():
    paths = ["/", "/tools", "/learn"] + TOOL_PATHS + ["/learn/" + a["slug"] for a in ARTICLES]
    items = ""
    for p in paths:
        items += "<url><loc>" + BASE_URL + p + "</loc><lastmod>2026-09-03</lastmod><changefreq>weekly</changefreq></url>"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>"
    return Response(xml, media_type="application/xml")

@router.get("/robots.txt")
async def robots():
    txt = "User-agent: *\\nAllow: /\\nDisallow: /api/\\nDisallow: /admin.html\\nDisallow: /app.html\\n\\nSitemap: " + BASE_URL + "/sitemap.xml\\n"
    return Response(txt, media_type="text/plain")
'''
open("backend/routers/site_routes.py", "w", encoding="utf-8").write(routes)
print("[REWRITTEN] site_routes.py with /learn CMS + sitemap.xml + robots.txt")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 4: CMS engine, 2 pillar articles with schema, dynamic sitemap + robots"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
