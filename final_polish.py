import subprocess, os

# === 1. CREATE careers.html ===
careers_html = """{% extends "base.html" %}
{% block title %}Cybersecurity Career Roadmaps | GRCWithGaurav{% endblock %}
{% block description %}Step-by-step career roadmaps for SOC Analyst, GRC Analyst, and Penetration Tester roles. Skills, certifications, portfolio projects, and interview prep.{% endblock %}
{% block content %}
<div style="max-width:1000px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Cybersecurity Career Roadmaps</h1>
 <p style="color:var(--muted);font-size:1.1rem;line-height:1.6">Three proven paths into cybersecurity. Pick the one that matches your background and follow it step by step.</p>

 <div class="grid-3" style="margin-top:2rem">
  <div class="card">
   <h3>SOC Analyst Path</h3>
   <p style="color:#c9c9c9;font-size:.9rem">Monitor, triage, and respond to security alerts. Best for: people who like fast-paced investigation and shift work.</p>
   <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem">
    <li>Months 1-2: Network+ / Security+ fundamentals</li>
    <li>Months 3-4: SIEM hands-on (Splunk free tier, ELK)</li>
    <li>Months 5-6: Detection labs + CTF practice</li>
    <li>Month 7+: Apply to Tier 1 SOC roles</li>
   </ul>
   <a href="/learn/what-does-soc-analyst-do" style="color:var(--accent);font-size:.9rem">Read the full SOC guide &rarr;</a>
  </div>
  <div class="card">
   <h3>GRC Analyst Path</h3>
   <p style="color:#c9c9c9;font-size:.9rem">Governance, risk, and compliance. Best for: detail-oriented people from audit, legal, finance, or ops backgrounds. No coding required.</p>
   <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem">
    <li>Months 1-2: Learn GRC + ISO 27001 basics</li>
    <li>Months 3-4: Build risk register + policy portfolio</li>
    <li>Months 5-6: ISO 27001 Lead Implementer or Security+</li>
    <li>Month 7+: Apply to GRC / compliance roles</li>
   </ul>
   <a href="/learn/grc-analyst-career-roadmap" style="color:var(--accent);font-size:.9rem">Read the full GRC guide &rarr;</a>
  </div>
  <div class="card">
   <h3>Penetration Tester Path</h3>
   <p style="color:#c9c9c9;font-size:.9rem">Offensive security testing. Best for: people who love breaking things and have strong networking + scripting skills. Longest path of the three.</p>
   <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem">
    <li>Months 1-3: Networking + Linux + Python basics</li>
    <li>Months 4-8: TryHackMe / HackTheBox grind</li>
    <li>Months 9-12: OSCP prep + bug bounty practice</li>
    <li>Year 2+: Apply to junior pentest roles</li>
   </ul>
   <a href="/learn/best-cybersecurity-certifications-beginners-2026" style="color:var(--accent);font-size:.9rem">See which certs matter &rarr;</a>
  </div>
 </div>

 <div class="card" style="padding:2rem;margin-top:2.5rem;text-align:center;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <h2 style="color:#fff;margin-top:0">Not sure which path fits you?</h2>
  <p style="color:var(--muted);max-width:600px;margin:0 auto 1.5rem">CyberVerse AI assesses your current skills and builds a personalized 6-month roadmap based on your exact gaps - not a generic checklist.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Get My Personalized Roadmap</a>
 </div>

 <div class="section" style="padding:2rem 0 0">
  <h2 style="text-align:left">Supporting guides</h2>
  <div class="grid-3">
   <div class="card"><h3 style="font-size:1rem">How to Start a GRC Career</h3><p style="font-size:.85rem;color:#c9c9c9">The exact first 90 days for career changers.</p><a href="/learn/how-to-start-grc-career" style="font-size:.85rem">Read &rarr;</a></div>
   <div class="card"><h3 style="font-size:1rem">Build a Portfolio That Gets Hired</h3><p style="font-size:.85rem;color:#c9c9c9">Five artifacts that beat 20 GitHub repos.</p><a href="/learn/cybersecurity-portfolio-guide" style="font-size:.85rem">Read &rarr;</a></div>
   <div class="card"><h3 style="font-size:1rem">Salary Expectations 2026</h3><p style="font-size:.85rem;color:#c9c9c9">Real numbers by role and experience level.</p><a href="/learn/cybersecurity-salary-india-2026" style="font-size:.85rem">Read &rarr;</a></div>
  </div>
 </div>
</div>
{% endblock %}
"""

with open("backend/templates/careers.html", "w", encoding="utf-8") as f:
    f.write(careers_html)
print("[CREATED] careers.html with 3 career paths")

# === 2. UPDATE /careers ROUTE ===
sr = "backend/routers/site_routes.py"
c = open(sr, encoding="utf-8").read()

old_careers = '''@router.get("/careers", response_class=HTMLResponse)
async def careers_page(request: Request):
    # Redirects to homepage until Careers pages are built in a future phase
    return RedirectResponse(url="/", status_code=302)'''

new_careers = '''@router.get("/careers", response_class=HTMLResponse)
async def careers_page(request: Request):
    return templates.TemplateResponse("careers.html", {"request": request})'''

if old_careers in c:
    c = c.replace(old_careers, new_careers, 1)
    open(sr, "w", encoding="utf-8").write(c)
    print("[UPDATED] /careers route now serves careers.html")
else:
    print("[SKIP] /careers route pattern not found")

# === 3. READING PROGRESS BAR ON ARTICLES ===
article_html = "backend/templates/learn/article.html"
c = open(article_html, encoding="utf-8").read()

progress_bar = """<div id="progress-bar" style="position:fixed;top:0;left:0;height:3px;background:var(--accent);width:0%;z-index:1000"></div>
<script>
window.addEventListener('scroll', () => {
  const h = document.documentElement;
  const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
});
</script>
"""

if "progress-bar" not in c:
    c = c.replace("{% block content %}", "{% block content %}\n" + progress_bar, 1)
    open(article_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] article.html - reading progress bar added")
else:
    print("[SKIP] Progress bar already present")

# === 4. TESTIMONIALS NEAR CYBERVERSE + B2B SECTIONS ===
index_html = "backend/templates/index.html"
c = open(index_html, encoding="utf-8").read()

# Add testimonial under CyberVerse AI section
cyberverse_testimonial = '''    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Stop guessing. Start getting hired.</h3>
        <p>AI mock interviews, automated resume rewrites, and 6-month SOC/GRC roadmaps tailored to your exact skill gaps.</p>
        <a href="/app.html" class="btn-primary" style="display:inline-block; margin-top:1rem;">Launch CyberVerse AI</a>
    </div>
    <p style="text-align:center;color:var(--muted);font-style:italic;margin-top:1.2rem;font-size:.92rem">"The mock interviews exposed gaps I didn't know I had. Landed a SOC analyst role 3 weeks later." - Priya S., SOC Analyst</p>'''

old_cyberverse = '''    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Stop guessing. Start getting hired.</h3>
        <p>AI mock interviews, automated resume rewrites, and 6-month SOC/GRC roadmaps tailored to your exact skill gaps.</p>
        <a href="/app.html" class="btn-primary" style="display:inline-block; margin-top:1rem;">Launch CyberVerse AI</a>
    </div>'''

if old_cyberverse in c and "Priya S." not in c.split("Free Cybersecurity")[0]:
    c = c.replace(old_cyberverse, cyberverse_testimonial, 1)
    print("[UPDATED] Testimonial added under CyberVerse AI section")

# Add testimonial under B2B section
b2b_testimonial = '''    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Get a Free GRC Assessment</h3>
        <p>For businesses: a scoped review of your current posture, priority gaps and a 90-day roadmap - no obligation.</p>
        <a href="/b2b" class="btn-primary" style="display:inline-block; margin-top:1rem;">Get a Free GRC Assessment</a>
    </div>
    <p style="text-align:center;color:var(--muted);font-style:italic;margin-top:1.2rem;font-size:.92rem">"The ISO 27001 risk calculator saved us hours. Our auditor actually praised the documentation." - Rahul K., GRC Consultant</p>'''

old_b2b = '''    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Get a Free GRC Assessment</h3>
        <p>For businesses: a scoped review of your current posture, priority gaps and a 90-day roadmap - no obligation.</p>
        <a href="/b2b" class="btn-primary" style="display:inline-block; margin-top:1rem;">Get a Free GRC Assessment</a>
    </div>'''

if old_b2b in c and "Rahul K." not in c:
    c = c.replace(old_b2b, b2b_testimonial, 1)
    print("[UPDATED] Testimonial added under B2B section")

open(index_html, "w", encoding="utf-8").write(c)

# === 5. PERSISTENT FREE RESOURCES CTA ===
base_html = "backend/templates/base.html"
c = open(base_html, encoding="utf-8").read()

sticky_cta = """
<div id="free-cta" style="position:fixed;bottom:1.2rem;right:1.2rem;z-index:999;display:none">
 <a href="/tools" style="display:flex;align-items:center;gap:.5rem;background:var(--accent);color:#000;padding:.7rem 1.2rem;border-radius:50px;font-weight:700;font-size:.9rem;box-shadow:0 4px 20px rgba(0,255,204,.35);text-decoration:none">
  🛠️ Free GRC Tools
 </a>
</div>
<script>
(function(){
  if (sessionStorage.getItem('cta_seen')) return;
  setTimeout(function(){
    var el = document.getElementById('free-cta');
    if (el) { el.style.display = 'block'; sessionStorage.setItem('cta_seen','1'); }
  }, 15000);
})();
</script>
"""

if "free-cta" not in c:
    c = c.replace("</body>", sticky_cta + "</body>", 1)
    open(base_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] base.html - persistent Free Tools CTA added (shows after 15s, once per session)")
else:
    print("[SKIP] Sticky CTA already present")

# === 6. COMMIT AND PUSH ===
try:
    compile(open(sr, encoding="utf-8").read(), sr, "exec")
    print("[COMPILE] site_routes.py verified clean")
except SyntaxError as e:
    print(f"[ABORT] Syntax error: {e}")
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Polish: careers page, reading progress bar, contextual testimonials, sticky CTA"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout if r.returncode == 0 else r.stderr}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
