import os
import re

print("=== PHASE 2: JINJA2 SETUP & MAIN SITE SHELL ===")

# 1. Update Requirements
print("[1/5] Updating requirements.txt...")
req_file = "requirements.txt"
reqs = open(req_file, "r", encoding="utf-8").read() if os.path.exists(req_file) else ""
new_deps = []
if "jinja2" not in reqs.lower(): new_deps.append("jinja2")
if "aiofiles" not in reqs.lower(): new_deps.append("aiofiles")
if new_deps:
    with open(req_file, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(new_deps) + "\n")
    os.system("backend\\venv\\Scripts\\pip.exe install " + " ".join(new_deps))

# 2. Create Templates Directory
print("[2/5] Creating template architecture...")
os.makedirs("backend/templates", exist_ok=True)

# 3. Write base.html (The Global Shell)
print("[3/5] Writing base.html (Nav + Footer + SEO)...")
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}GRCWithGaurav | Cybersecurity, GRC & AI Platform{% endblock %}</title>
    <meta name="description" content="{% block description %}Learn cybersecurity, prepare for certifications, build your career and automate GRC tasks with practical guides and AI-powered tools.{% endblock %}">
    <link rel="canonical" href="{% block canonical %}https://grcwithgaurav.com{% endblock %}">
    
    <!-- Open Graph / Social -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{% block title %}GRCWithGaurav | Cybersecurity, GRC & AI Platform{% endblock %}">
    <meta property="og:description" content="{% block description %}Learn cybersecurity, prepare for certifications, build your career and automate GRC tasks.{% endblock %}">
    
    <style>
        :root { --bg: #0a0a0a; --surface: #111; --accent: #00ffcc; --text: #e0e0e0; --muted: #888; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.6; }
        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }
        
        /* Navigation */
        .nav { background: rgba(10,10,10,0.95); backdrop-filter: blur(8px); border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 100; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        .nav-brand { font-weight: 800; font-size: 1.2rem; color: #fff; }
        .nav-brand span { color: var(--accent); }
        .nav-links { display: flex; gap: 1.5rem; }
        .nav-links a { color: var(--text); font-weight: 500; font-size: 0.95rem; }
        .nav-links a:hover { color: var(--accent); text-decoration: none; }
        .nav-cta { background: var(--accent); color: #000; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 700; font-size: 0.9rem; }
        
        /* Hero */
        .hero { text-align: center; padding: 5rem 2rem; max-width: 900px; margin: 0 auto; }
        .hero h1 { font-size: 3rem; line-height: 1.2; margin-bottom: 1rem; color: #fff; }
        .hero h1 span { color: var(--accent); }
        .hero p { font-size: 1.2rem; color: var(--muted); max-width: 700px; margin: 0 auto 2rem; }
        .btn-group { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
        .btn-primary { background: var(--accent); color: #000; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 1rem; }
        .btn-secondary { background: transparent; border: 1px solid #444; color: #fff; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 1rem; }
        
        /* Sections */
        .section { padding: 4rem 2rem; max-width: 1100px; margin: 0 auto; }
        .section h2 { font-size: 2rem; color: #fff; margin-bottom: 2rem; text-align: center; }
        .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
        .card { background: var(--surface); border: 1px solid #222; border-radius: 12px; padding: 1.5rem; transition: border-color 0.2s; }
        .card:hover { border-color: var(--accent); }
        .card h3 { color: var(--accent); margin-top: 0; }
        
        /* Footer */
        .footer { background: #050505; border-top: 1px solid #222; padding: 3rem 2rem; text-align: center; color: var(--muted); font-size: 0.9rem; margin-top: 4rem; }
        .footer-links { display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 1rem; flex-wrap: wrap; }
        
        @media (max-width: 768px) {
            .nav-links { display: none; } /* Hide for mobile MVP, add hamburger later */
            .hero h1 { font-size: 2rem; }
        }
    </style>
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="nav">
        <a href="/" class="nav-brand">GRC<span>WithGaurav</span></a>
        <div class="nav-links">
            <a href="/learn">Learn</a>
            <a href="/tools">Tools</a>
            <a href="/careers">Careers</a>
            <a href="/resources">Resources</a>
            <a href="/app.html" class="nav-cta">CyberVerse AI</a>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/disclaimer">Disclaimer</a>
            <a href="/b2b">For Businesses</a>
        </div>
        <p>&copy; 2026 GRCWithGaurav. Cybersecurity. GRC. AI. One Platform.</p>
    </footer>
</body>
</html>"""
with open("backend/templates/base.html", "w", encoding="utf-8") as f:
    f.write(base_html)

# 4. Write index.html (The New Homepage)
print("[4/5] Writing new SEO Homepage...")
index_html = """{% extends "base.html" %}
{% block title %}GRCWithGaurav | Cybersecurity, GRC & AI Platform{% endblock %}
{% block content %}
<section class="hero">
    <h1>Cybersecurity. GRC. AI. <span>One Platform.</span></h1>
    <p>Learn cybersecurity, prepare for certifications, build your career and automate GRC tasks with practical guides and AI-powered tools.</p>
    <div class="btn-group">
        <a href="/tools" class="btn-primary">Explore Free Tools</a>
        <a href="/app.html" class="btn-secondary">Try CyberVerse AI</a>
    </div>
</section>

<section class="section">
    <h2>Free Cybersecurity & GRC Tools</h2>
    <div class="grid-3">
        <div class="card"><h3>ISO 27001 Risk Calculator</h3><p>Calculate and document risk scores based on likelihood and impact.</p><a href="/tools/iso-risk-calculator">Use Tool &rarr;</a></div>
        <div class="card"><h3>CVSS Calculator</h3><p>Accurately score vulnerabilities using the CVSS v3.1 standard.</p><a href="/tools/cvss-calculator">Use Tool &rarr;</a></div>
        <div class="card"><h3>Resume ATS Checker</h3><p>See if your cybersecurity resume passes the automated bots.</p><a href="/tools/ats-checker">Use Tool &rarr;</a></div>
    </div>
</section>

<section class="section">
    <h2>CyberVerse AI: Your Personal Mentor</h2>
    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Stop guessing. Start getting hired.</h3>
        <p>AI mock interviews, automated resume rewrites, and 6-month SOC/GRC roadmaps tailored to your exact skill gaps.</p>
        <a href="/app.html" class="btn-primary" style="display:inline-block; margin-top:1rem;">Launch CyberVerse AI</a>
    </div>
</section>

<section class="section">
    <h2>Learn & Build Your Career</h2>
    <div class="grid-3">
        <div class="card"><h3>SOC & Incident Response</h3><p>Master SIEM, alert triage, and the MITRE ATT&CK framework.</p><a href="/learn/soc">Start Learning &rarr;</a></div>
        <div class="card"><h3>GRC & ISO 27001</h3><p>Understand audits, risk registers, and compliance frameworks.</p><a href="/learn/grc">Start Learning &rarr;</a></div>
        <div class="card"><h3>Career Roadmaps</h3><p>Step-by-step guides to landing your first Tier 1 or GRC role.</p><a href="/careers">View Roadmaps &rarr;</a></div>
    </div>
</section>
{% endblock %}"""
with open("backend/templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

# 5. Create Site Router & Patch main.py
print("[5/5] Wiring up FastAPI routes...")
os.makedirs("backend/routers", exist_ok=True)
router_code = """from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
@router.get("/tools", response_class=HTMLResponse)
@router.get("/careers", response_class=HTMLResponse)
@router.get("/resources", response_class=HTMLResponse)
async def placeholders(request: Request):
    # Simple placeholder for now so nav links don't 404
    return templates.TemplateResponse("index.html", {"request": request})
"""
with open("backend/routers/site_routes.py", "w", encoding="utf-8") as f:
    f.write(router_code)

# Patch main.py to include the router BEFORE static mounts
main_py = "backend/main.py"
if os.path.exists(main_py):
    content = open(main_py, "r", encoding="utf-8").read()
    if "site_routes" not in content:
        # Inject import and include_router near the top
        import_stmt = "from routers import site_routes\n"
        include_stmt = "app.include_router(site_routes.router)\n"
        
        # Find a safe place to inject (after app = FastAPI(...))
        content = re.sub(r'(app\s*=\s*FastAPI\([^)]*\))', r'\1\n' + import_stmt + include_stmt, content, count=1)
        open(main_py, "w", encoding="utf-8").write(content)
        print("[PATCHED] main.py updated with site_routes.")

print("\n=== COMMIT & PUSH ===")
os.system("git add -A")
os.system('git commit -m "Phase 2: Implement Jinja2 shell, global nav, and new SEO homepage"')
os.system("git push origin main")
print("\nPushed! Render will deploy the new architecture in ~60s.")
