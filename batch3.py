import os, subprocess, re

# === 1. HOMEPAGE NEWSLETTER SIGNUP ===
idx_html = "backend/templates/index.html"
c = open(idx_html, encoding="utf-8").read()

newsletter_block = """
<section class="section" style="background:linear-gradient(135deg,#0d1a16,#0a0a0a);border-radius:16px;border:1px solid var(--accent);margin:2rem auto;max-width:1100px;text-align:center;">
    <h2 style="margin-bottom:.5rem">Get one GRC tip + tool every week</h2>
    <p style="color:var(--muted);max-width:600px;margin:0 auto 1.5rem">Join cybersecurity professionals getting practical frameworks, tools, and career advice. No spam, just signal.</p>
    <div style="display:flex;gap:.5rem;max-width:440px;margin:0 auto">
      <input id="hero-nl-email" type="email" placeholder="you@company.com" style="flex:1;padding:.7rem 1rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;font-size:1rem">
      <button id="hero-nl-btn" style="background:var(--accent);color:#000;border:none;border-radius:8px;padding:.7rem 1.5rem;font-weight:700;cursor:pointer;font-size:1rem">Subscribe</button>
    </div>
    <p id="hero-nl-msg" style="font-size:.8rem;color:#666;margin-top:.5rem"></p>
</section>
<script>
document.getElementById('hero-nl-btn')?.addEventListener('click', async () => {
    const email = document.getElementById('hero-nl-email').value;
    const msg = document.getElementById('hero-nl-msg');
    if(!email || !email.includes('@')) { msg.textContent = 'Please enter a valid email.'; msg.style.color='#ff4444'; return; }
    msg.textContent = 'Subscribing...'; msg.style.color='#888';
    try {
        const r = await fetch('/api/analytics/newsletter/subscribe', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email})});
        const d = await r.json();
        if(d.ok || r.ok) { msg.textContent = 'Check your inbox to confirm!'; msg.style.color='var(--accent)'; }
        else { msg.textContent = 'Please use the footer form to subscribe.'; msg.style.color='#ff4444'; }
    } catch(e) { msg.textContent = 'Network error.'; msg.style.color='#ff4444'; }
});
</script>
"""

if "hero-nl-email" not in c:
    # Insert before the Tools section
    c = c.replace('<section class="section">\n    <h2>Free Cybersecurity & GRC Tools</h2>', 
                  newsletter_block + '\n<section class="section">\n    <h2>Free Cybersecurity & GRC Tools</h2>', 1)
    open(idx_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] index.html - prominent newsletter added")
else:
    print("[SKIP] Homepage newsletter already present")

# === 2. GENERAL CONTACT PAGE ===
contact_html = """{% extends "base.html" %}
{% block title %}Contact | GRCWithGaurav{% endblock %}
{% block description %}Get in touch with Gaurav Malhotra for career advice, B2B GRC consulting, or platform feedback.{% endblock %}
{% block content %}
<div style="max-width:700px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Get in touch</h1>
 <p style="color:var(--muted);font-size:1.05rem;line-height:1.6">Whether you're a student trying to break into GRC, a hiring manager, or a business needing ISO 27001 help - I read every message.</p>
 
 <div class="card" style="padding:2rem;margin-top:2rem">
  <h3 style="color:var(--accent);margin-top:0">Send a message</h3>
  <p style="color:#c9c9c9">The fastest way to reach me is via email. Click below to open your mail client with my address pre-filled.</p>
  
  <div style="display:grid;gap:1rem;margin-top:1.5rem">
   <a href="mailto:hello@mail.grcwithgaurav.com?subject=Career%20Advice%20Question" style="padding:1rem;background:#151515;border:1px solid #333;border-radius:8px;text-decoration:none;display:block">
    <strong style="color:#fff">🎓 Career / Interview Question</strong><br>
    <span style="color:var(--muted);font-size:.9rem">For students and job seekers</span>
   </a>
   <a href="mailto:b2b@mail.grcwithgaurav.com?subject=B2B%20GRC%20Consulting" style="padding:1rem;background:#151515;border:1px solid #333;border-radius:8px;text-decoration:none;display:block">
    <strong style="color:#fff">🏢 B2B / Enterprise Consulting</strong><br>
    <span style="color:var(--muted);font-size:.9rem">For ISO 27001, risk assessments, and security architecture</span>
   </a>
   <a href="mailto:support@mail.grcwithgaurav.com?subject=Platform%20Feedback" style="padding:1rem;background:#151515;border:1px solid #333;border-radius:8px;text-decoration:none;display:block">
    <strong style="color:#fff">🛠️ Platform Bug / Feedback</strong><br>
    <span style="color:var(--muted);font-size:.9rem">Found a broken tool or have a feature request?</span>
   </a>
  </div>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:1.5rem;text-align:center">
  <p style="color:var(--muted);margin:0">Prefer social? Connect with me on <a href="https://linkedin.com/in/gauravmalhotracybersecurity" target="_blank" style="color:var(--accent)">LinkedIn</a> or <a href="https://twitter.com/gauravmalhotra" target="_blank" style="color:var(--accent)">Twitter</a>.</p>
 </div>
</div>
{% endblock %}
"""

with open("backend/templates/contact.html", "w", encoding="utf-8") as f:
    f.write(contact_html)
print("[UPDATED] contact.html - general contact page (student + B2B friendly)")

# === 3. FAQ PAGE ===
faq_html = """{% extends "base.html" %}
{% block title %}Frequently Asked Questions | GRCWithGaurav{% endblock %}
{% block description %}Answers to common questions about GRC careers, CyberVerse AI, ISO 27001, and breaking into cybersecurity.{% endblock %}
{% block head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "What is GRC in cybersecurity?", "acceptedAnswer": { "@type": "Answer", "text": "GRC stands for Governance, Risk, and Compliance. It is the practice of aligning IT security with business goals, managing risks, and ensuring compliance with frameworks like ISO 27001, SOC 2, and HIPAA." } },
    { "@type": "Question", "name": "Do I need coding skills for a GRC role?", "acceptedAnswer": { "@type": "Answer", "text": "No. GRC roles focus on policy, risk assessment, audits, and compliance. While basic technical understanding is helpful, you do not need to write code or configure firewalls." } },
    { "@type": "Question", "name": "What is CyberVerse AI?", "acceptedAnswer": { "@type": "Answer", "text": "CyberVerse AI is an AI-powered mock interview and career coaching platform. It simulates real hiring manager interviews for SOC, GRC, and Infosec roles, grading your answers and providing actionable feedback." } },
    { "@type": "Question", "name": "Are the tools on this site really free?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. The 10+ GRC tools (risk calculators, policy generators, resume checkers) are 100% free. CyberVerse AI offers a free tier, with Pro (499) and Premium (999) lifetime tiers for advanced features like AI mock interviews and verifiable certificates." } },
    { "@type": "Question", "name": "How do I transition into cybersecurity from another field?", "acceptedAnswer": { "@type": "Answer", "text": "Focus on provable skills over just collecting certificates. Build a portfolio (GitHub, blog posts), use our free tools to create audit-ready artifacts, and practice explaining your reasoning out loud using CyberVerse AI." } }
  ]
}
</script>
{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Frequently Asked Questions</h1>
 <p style="color:var(--muted);font-size:1.05rem">Quick answers about GRC, cybersecurity careers, and the platform.</p>
 
 <div style="margin-top:2rem">
  <details class="card" style="padding:1.2rem;margin-bottom:1rem;cursor:pointer">
   <summary style="color:#fff;font-weight:600;font-size:1.1rem">What is GRC in cybersecurity?</summary>
   <p style="color:#c9c9c9;margin-top:.8rem;line-height:1.6">GRC stands for Governance, Risk, and Compliance. It is the practice of aligning IT security with business goals, managing risks, and ensuring compliance with frameworks like ISO 27001, SOC 2, and HIPAA. It's less about configuring firewalls and more about managing business risk.</p>
  </details>
  <details class="card" style="padding:1.2rem;margin-bottom:1rem;cursor:pointer">
   <summary style="color:#fff;font-weight:600;font-size:1.1rem">Do I need coding skills for a GRC role?</summary>
   <p style="color:#c9c9c9;margin-top:.8rem;line-height:1.6">No. GRC roles focus on policy, risk assessment, audits, and compliance. While basic technical understanding (like knowing what a firewall does) is helpful, you do not need to write code, script, or configure infrastructure.</p>
  </details>
  <details class="card" style="padding:1.2rem;margin-bottom:1rem;cursor:pointer">
   <summary style="color:#fff;font-weight:600;font-size:1.1rem">What is CyberVerse AI?</summary>
   <p style="color:#c9c9c9;margin-top:.8rem;line-height:1.6">CyberVerse AI is an AI-powered mock interview and career coaching platform. It simulates real hiring manager interviews for SOC, GRC, and Infosec roles, grading your spoken/written answers and providing actionable feedback to help you improve.</p>
  </details>
  <details class="card" style="padding:1.2rem;margin-bottom:1rem;cursor:pointer">
   <summary style="color:#fff;font-weight:600;font-size:1.1rem">Are the tools on this site really free?</summary>
   <p style="color:#c9c9c9;margin-top:.8rem;line-height:1.6">Yes. The 10+ GRC tools (risk calculators, policy generators, resume checkers) are 100% free. CyberVerse AI offers a free tier, with Pro (499) and Premium (999) lifetime tiers for advanced features like unlimited AI mock interviews and verifiable certificates.</p>
  </details>
  <details class="card" style="padding:1.2rem;margin-bottom:1rem;cursor:pointer">
   <summary style="color:#fff;font-weight:600;font-size:1.1rem">How do I transition into cybersecurity from another field?</summary>
   <p style="color:#c9c9c9;margin-top:.8rem;line-height:1.6">Focus on provable skills over just collecting certificates. Build a portfolio (GitHub, blog posts), use our free tools to create audit-ready artifacts, and practice explaining your reasoning out loud using CyberVerse AI. Hiring managers want to see how you think, not just what exams you passed.</p>
  </details>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:2rem;text-align:center;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <h3 style="color:#fff;margin-top:0">Still have questions?</h3>
  <p style="color:var(--muted)">Reach out directly via our contact page.</p>
  <a href="/contact" class="btn-primary" style="display:inline-block;margin-top:.5rem">Contact Gaurav</a>
 </div>
</div>
{% endblock %}
"""

with open("backend/templates/faq.html", "w", encoding="utf-8") as f:
    f.write(faq_html)
print("[CREATED] faq.html with FAQPage schema")

# Add /faq route to site_routes.py
sr = "backend/routers/site_routes.py"
c = open(sr, encoding="utf-8").read()
if '"/faq"' not in c:
    faq_route = """

@router.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})
"""
    c += faq_route
    open(sr, "w", encoding="utf-8").write(c)
    print("[UPDATED] site_routes.py - /faq route added")

# === 4. ORGANIZATION SCHEMA (base.html) ===
base_html = open("backend/templates/base.html", encoding="utf-8").read()
org_schema = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "GRCWithGaurav",
  "url": "https://grcwithgaurav.com",
  "logo": "https://grcwithgaurav.com/static/og-default.jpg",
  "description": "Practical cybersecurity, GRC, and AI tools for security teams and job seekers.",
  "founder": {
    "@type": "Person",
    "name": "Gaurav Malhotra"
  },
  "sameAs": [
    "https://linkedin.com/in/gauravmalhotracybersecurity",
    "https://twitter.com/gauravmalhotra"
  ]
}
</script>
"""

if '"@type": "Organization"' not in base_html:
    base_html = base_html.replace('<meta property="og:site_name" content="GRCWithGaurav">', 
                                  '<meta property="og:site_name" content="GRCWithGaurav">' + org_schema, 1)
    open("backend/templates/base.html", "w", encoding="utf-8").write(base_html)
    print("[UPDATED] base.html - Organization schema added")

# === 5. COMMIT AND PUSH ===
try:
    compile(open(sr, encoding="utf-8").read(), sr, "exec")
    print("[COMPILE] site_routes.py verified clean")
except SyntaxError as e:
    print(f"[ABORT] Syntax error in site_routes.py: {e}")
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
result = subprocess.run(["git", "commit", "-m", "Conversion: homepage newsletter, general contact, FAQ page, org schema"], capture_output=True, text=True)
print(f"\n[COMMIT] {result.stdout if result.returncode == 0 else result.stderr}")

result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if result.returncode == 0:
    print("[PUSHED] Batch 3 deploying to Render")
else:
    print(f"[PUSH FAILED] {result.stderr}")
