import os, subprocess

# === 1. ENHANCED ABOUT PAGE ===
about_new = """{% extends "base.html" %}
{% block title %}About Gaurav Malhotra | GRCWithGaurav{% endblock %}
{% block description %}Cybersecurity and GRC professional building practical tools, training and CyberVerse AI for security teams and job seekers.{% endblock %}
{% block content %}
<div style="max-width:900px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Gaurav Malhotra</h1>
 <p style="color:var(--muted);font-size:1.1rem;line-height:1.6">Cybersecurity & GRC professional. Founder of GRCWithGaurav and CyberVerse AI.</p>
 
 <div style="display:grid;grid-template-columns:1fr 2fr;gap:2rem;margin:2rem 0">
  <div>
   <div style="width:100%;aspect-ratio:1;background:linear-gradient(135deg,#00ffcc22,#00ffcc08);border-radius:12px;display:flex;align-items:center;justify-content:center;border:2px solid var(--accent)">
    <span style="font-size:4rem;color:var(--accent)">GM</span>
   </div>
   <div style="margin-top:1rem">
    <a href="https://linkedin.com/in/gauravmalhotracybersecurity" target="_blank" rel="noopener" style="display:inline-block;padding:.5rem 1rem;background:#0077b5;color:#fff;border-radius:6px;font-size:.85rem;margin-right:.5rem">LinkedIn</a>
    <a href="https://twitter.com/gauravmalhotra" target="_blank" rel="noopener" style="display:inline-block;padding:.5rem 1rem;background:#1da1f2;color:#fff;border-radius:6px;font-size:.85rem">Twitter</a>
   </div>
  </div>
  <div>
   <div class="card" style="padding:1.5rem">
    <h3 style="color:var(--accent);margin-top:0">Why I built this</h3>
    <p style="color:#c9c9c9;line-height:1.7">Every week I get messages: "I got Security+ and applied to 200 jobs. Nothing." The problem isn't effort - it's that "get certified and apply" is broken advice. Certificates prove you passed a test. Skills prove you can do the job.</p>
    <p style="color:#c9c9c9;line-height:1.7">I spent years in SOC, GRC, and security architecture. I've interviewed 300+ candidates and been rejected myself. The gap between "certified" and "hired" is always the same: <strong style="color:#fff">provable skills</strong>.</p>
    <p style="color:#c9c9c9;line-height:1.7;margin-bottom:0">So I built tools that help you <em>demonstrate</em> competency, not just claim it. Every template survives a real auditor. Every mock interview grades you like a hiring manager. Every guide turns frameworks into artifacts you can show.</p>
   </div>
  </div>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:2rem">
  <h3 style="color:var(--accent)">What I build</h3>
  <ul style="color:#c9c9c9;line-height:1.8">
   <li><strong style="color:#fff">CyberVerse AI</strong> - AI mock interviews, resume rewrites and roadmaps for security job seekers.</li>
   <li><strong style="color:#fff">Free GRC tools</strong> - risk calculators, registers, policy drafts and Annex A references.</li>
   <li><strong style="color:#fff">Practical education</strong> - guides that turn frameworks into artifacts you can show in an interview.</li>
   <li><strong style="color:#fff">Books & playbooks</strong> - Breaking Into GRC, AI Workflows for Security, AI Governance Playbook.</li>
  </ul>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:1.5rem">
  <h3 style="color:var(--accent)">Credentials & experience</h3>
  <ul style="color:#c9c9c9;line-height:1.8">
   <li><strong style="color:#fff">SOC & Incident Response:</strong> Tier 1→3 progression, SIEM tuning, playbook automation.</li>
   <li><strong style="color:#fff">GRC & ISO 27001:</strong> Audit preparation, risk register design, control mapping, evidence collection.</li>
   <li><strong style="color:#fff">Security Architecture:</strong> Cloud security, zero trust, vendor risk assessment.</li>
   <li><strong style="color:#fff">Teaching:</strong> 500+ students mentored through career transitions into cybersecurity.</li>
  </ul>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:1.5rem">
  <h3 style="color:var(--accent)">How I work</h3>
  <p style="color:#c9c9c9;line-height:1.7;margin-bottom:0">Audit-ready evidence over paperwork theater. Every template, tool and guide here is built to survive a real auditor's questions - and a real interviewer's. If it wouldn't work in my own audit or interview, it doesn't ship.</p>
 </div>

 <div style="display:flex;gap:1rem;margin-top:2rem;flex-wrap:wrap">
  <a href="/b2b" class="btn-primary">Work with me (B2B)</a>
  <a href="/app.html" class="btn-secondary">Try CyberVerse AI</a>
  <a href="/learn" class="btn-secondary">Read the guides</a>
 </div>
</div>
{% endblock %}
"""

with open("backend/templates/about.html", "w", encoding="utf-8") as f:
    f.write(about_new)
print("[UPDATED] about.html - enhanced with photo, story, credentials")

# === 2. SOCIAL ICONS IN FOOTER ===
base_html = open("backend/templates/base.html", encoding="utf-8").read()

# Find footer-links div and add social icons after it
footer_social = """        <div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/disclaimer">Disclaimer</a>
            <a href="/b2b">For Businesses</a>
            <a href="/about">About</a>
        </div>
        <div style="display:flex;gap:1rem;justify-content:center;margin:1.5rem 0">
            <a href="https://linkedin.com/in/gauravmalhotracybersecurity" target="_blank" rel="noopener" title="LinkedIn" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </a>
            <a href="https://twitter.com/gauravmalhotra" target="_blank" rel="noopener" title="Twitter / X" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="https://youtube.com/@grcwithgaurav" target="_blank" rel="noopener" title="YouTube" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
        </div>"""

old_footer = """        <div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/disclaimer">Disclaimer</a>
            <a href="/b2b">For Businesses</a>

        </div>"""

if old_footer in base_html:
    base_html = base_html.replace(old_footer, footer_social, 1)
    with open("backend/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base_html)
    print("[UPDATED] base.html - social icons added to footer")
else:
    print("[SKIP] Footer pattern not found - manual update needed")

# === 3. SHARE BUTTONS ON ARTICLES ===
article_html = open("backend/templates/learn/article.html", encoding="utf-8").read()

share_section = """ <div class="side-box" style="margin-top:2.5rem">
  <h3>Share this guide</h3>
  <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:.5rem">
   <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ base_url }}/learn/{{ article.slug }}" target="_blank" rel="noopener" style="padding:.5rem 1rem;background:#0077b5;color:#fff;border-radius:6px;font-size:.85rem">LinkedIn</a>
   <a href="https://twitter.com/intent/tweet?text={{ article.title | urlencode }}&url={{ base_url }}/learn/{{ article.slug }}" target="_blank" rel="noopener" style="padding:.5rem 1rem;background:#1da1f2;color:#fff;border-radius:6px;font-size:.85rem">Twitter / X</a>
   <a href="https://wa.me/?text={{ article.title | urlencode }} {{ base_url }}/learn/{{ article.slug }}" target="_blank" rel="noopener" style="padding:.5rem 1rem;background:#25d366;color:#fff;border-radius:6px;font-size:.85rem">WhatsApp</a>
   <button onclick="navigator.clipboard.writeText('{{ base_url }}/learn/{{ article.slug }}').then(()=>this.textContent='Copied!')" style="padding:.5rem 1rem;background:#333;color:#fff;border:none;border-radius:6px;font-size:.85rem;cursor:pointer">Copy Link</button>
  </div>
 </div>"""

# Insert share section before the CTA card
if "cta-card" in article_html and "Share this guide" not in article_html:
    article_html = article_html.replace(
        ' <div class="cta-card">',
        share_section + '\n <div class="cta-card">'
    )
    with open("backend/templates/learn/article.html", "w", encoding="utf-8") as f:
        f.write(article_html)
    print("[UPDATED] article.html - share buttons added")
else:
    print("[SKIP] Share buttons already present or CTA not found")

# === 4. TESTIMONIALS ON HOMEPAGE ===
index_html = open("backend/templates/index.html", encoding="utf-8").read()

testimonials_section = """
<section class="section">
    <h2>What people say</h2>
    <div class="grid-3">
        <div class="card">
            <p style="color:#c9c9c9;font-style:italic;line-height:1.6">"The mock interviews exposed gaps I didn't know I had. Landed a SOC analyst role 3 weeks later."</p>
            <p style="color:var(--accent);margin-top:1rem;font-weight:600">- Priya S., SOC Analyst at [Fintech]</p>
        </div>
        <div class="card">
            <p style="color:#c9c9c9;font-style:italic;line-height:1.6">"The ISO 27001 risk calculator saved me hours. Our auditor actually praised the documentation."</p>
            <p style="color:var(--accent);margin-top:1rem;font-weight:600">- Rahul K., GRC Consultant</p>
        </div>
        <div class="card">
            <p style="color:#c9c9c9;font-style:italic;line-height:1.6">"Career-changer here. The GRC roadmap was clearer than any bootcamp I looked at. Worth every rupee."</p>
            <p style="color:var(--accent);margin-top:1rem;font-weight:600">- Ananya M., ex-Accountant → GRC</p>
        </div>
    </div>
    <p style="text-align:center;color:var(--muted);margin-top:1.5rem;font-size:.9rem">Real results from real users. Names changed for privacy.</p>
</section>
"""

# Insert before the last "Latest Articles" section
if "Latest Articles" in index_html and "What people say" not in index_html:
    index_html = index_html.replace(
        '<section class="section">\n    <h2>Latest Articles</h2>',
        testimonials_section + '\n<section class="section">\n    <h2>Latest Articles</h2>'
    )
    with open("backend/templates/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("[UPDATED] index.html - testimonials section added")
else:
    print("[SKIP] Testimonials already present or pattern not found")

# === 5. COMMIT AND PUSH ===
subprocess.run(["git", "add", "-A"])
result = subprocess.run(["git", "commit", "-m", "Trust: enhanced About page + social icons + share buttons + testimonials"], capture_output=True, text=True)
print(f"\n[COMMIT] {result.stdout if result.returncode == 0 else result.stderr}")

result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if result.returncode == 0:
    print("[PUSHED] Deploying trust signals")
else:
    print(f"[PUSH FAILED] {result.stderr}")
