import glob, os, subprocess, re
skip = ("venv", "node_modules", ".git")

tdir = None
for root, dirs, files in os.walk("."):
    if any(t in root for t in skip): continue
    if os.path.basename(root) == "templates" and "backend" in root.replace("\\", "/"):
        tdir = root; break

privacy = """{% extends "base.html" %}
{% block title %}Privacy Policy | GRCWithGaurav{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem;color:#c9c9c9;line-height:1.7">
<h1 style="color:#fff">Privacy Policy</h1>
<p style="color:var(--muted)">Last updated: 8 September 2026</p>
<h3 style="color:#fff">1. What we collect</h3>
<ul>
<li><strong>Account data:</strong> name, email, hashed password when you register on CyberVerse AI.</li>
<li><strong>Profile &amp; practice data:</strong> resume text you submit, learning goals, certifications, interview and lab activity, XP and streaks.</li>
<li><strong>Usage analytics:</strong> first-party events (tool runs, page visits) used to improve the product.</li>
<li><strong>Business enquiries:</strong> details you submit via the B2B assessment form or newsletter signup.</li>
</ul>
<h3 style="color:#fff">2. Payments</h3>
<p>Payments are processed by <strong>Razorpay</strong>. We never see or store your card number, UPI PIN or banking credentials. We store only your plan, payment status and order/reference IDs.</p>
<h3 style="color:#fff">3. Email</h3>
<p>Transactional and newsletter emails are sent via <strong>Resend</strong>. Every marketing email contains a one-click unsubscribe link.</p>
<h3 style="color:#fff">4. Cookies &amp; local storage</h3>
<p>We use browser local storage for your session token and learning progress. We do not run third-party advertising trackers.</p>
<h3 style="color:#fff">5. How we use your data</h3>
<ul>
<li>Deliver and personalise the service (feedback, roadmaps, scores).</li>
<li>Support you and process refunds under our <a href="/refund-policy" style="color:var(--accent)">Refund Policy</a>.</li>
<li>Send product updates you opted into.</li>
<li>Improve tools using aggregated, anonymised usage patterns.</li>
</ul>
<h3 style="color:#fff">6. Sharing</h3>
<p>We share data only with processors required to run the service (Render hosting, Razorpay payments, Resend email). We <strong>never sell</strong> personal data.</p>
<h3 style="color:#fff">7. Retention &amp; your rights</h3>
<p>You may request export or deletion of your account data at any time by emailing <strong>hello@grcwithgaurav.com</strong>. We action valid requests within 30 days.</p>
<h3 style="color:#fff">8. Security</h3>
<p>Passwords are hashed, traffic is HTTPS-only, and admin endpoints are secret-protected. No method of transmission is 100% secure; we apply industry-standard care.</p>
<h3 style="color:#fff">9. Children</h3>
<p>The service is intended for users aged 16 and above.</p>
<h3 style="color:#fff">10. Changes</h3>
<p>Material changes will be posted here with an updated date. Continued use constitutes acceptance.</p>
</div>
{% endblock %}"""

terms = """{% extends "base.html" %}
{% block title %}Terms of Service | GRCWithGaurav{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem;color:#c9c9c9;line-height:1.7">
<h1 style="color:#fff">Terms of Service</h1>
<p style="color:var(--muted)">Last updated: 8 September 2026</p>
<h3 style="color:#fff">1. Acceptance</h3>
<p>By accessing grcwithgaurav.com or using CyberVerse AI you agree to these Terms, our <a href="/privacy" style="color:var(--accent)">Privacy Policy</a> and <a href="/refund-policy" style="color:var(--accent)">Refund Policy</a>.</p>
<h3 style="color:#fff">2. The service</h3>
<p>GRCWithGaurav (CyberVerse AI) provides AI-powered career training: mock interviews, resume analysis, study tools and educational content for cybersecurity and GRC roles. It is an <strong>educational platform</strong>, not a certification body or recruitment agency.</p>
<h3 style="color:#fff">3. Accounts</h3>
<p>You must provide accurate information, keep your credentials confidential, and use one account per person. You are responsible for activity under your account.</p>
<h3 style="color:#fff">4. Plans &amp; payments</h3>
<ul>
<li>Pro and Premium are one-time lifetime purchases priced in Indian Rupees; no auto-renewal.</li>
<li>Payments are processed by Razorpay; refunds follow the <a href="/refund-policy" style="color:var(--accent)">Refund Policy</a>.</li>
<li>Free-tier limits apply until upgrade.</li>
</ul>
<h3 style="color:#fff">5. Acceptable use</h3>
<p>You agree not to: resell or redistribute the service; scrape or reverse-engineer it; submit unlawful, plagiarised or malicious content; abuse AI features to generate harmful material; or share premium credentials with others.</p>
<h3 style="color:#fff">6. Intellectual property</h3>
<p>All platform content, tools and branding belong to GRCWithGaurav. Content you submit remains yours; you grant us a limited licence to process it solely to provide the service.</p>
<h3 style="color:#fff">7. AI outputs</h3>
<p>Interview feedback, scores and resume analysis are machine-generated guidance. They are provided "as is", may contain errors, and are not professional, legal, certification or hiring advice.</p>
<h3 style="color:#fff">8. Termination</h3>
<p>We may suspend accounts that breach these Terms. You may stop using the service at any time.</p>
<h3 style="color:#fff">9. Liability</h3>
<p>To the maximum extent permitted by law, our liability is limited to the amount you paid for the service. We are not liable for career outcomes, exam results or hiring decisions.</p>
<h3 style="color:#fff">10. Governing law</h3>
<p>These Terms are governed by the laws of India, with courts of New Delhi having exclusive jurisdiction.</p>
<h3 style="color:#fff">11. Contact</h3>
<p>Questions: hello@grcwithgaurav.com.</p>
</div>
{% endblock %}"""

disclaimer = """{% extends "base.html" %}
{% block title %}Disclaimer | GRCWithGaurav{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem;color:#c9c9c9;line-height:1.7">
<h1 style="color:#fff">Disclaimer</h1>
<p style="color:var(--muted)">Last updated: 8 September 2026</p>
<h3 style="color:#fff">Educational purpose only</h3>
<p>All content, tools, scores and certificates on this site are for <strong>education and skill practice</strong>. Nothing here constitutes legal, accounting, audit, certification or employment advice.</p>
<h3 style="color:#fff">AI-generated outputs</h3>
<p>Mock interviews, resume feedback and mentor responses are generated by AI. They can be incomplete or incorrect. Verify critical decisions against official sources (ISO/IEC, NIST, CompTIA, vendor documentation).</p>
<h3 style="color:#fff">No accreditation or affiliation</h3>
<p>CyberVerse AI scorecards and certificates are internal skill indicators. They are <strong>not accredited certifications</strong> and we are not affiliated with, endorsed by, or partnered with ISO, CompTIA, ISC2, EC-Council, Splunk, Microsoft or any other trademark holder. All trademarks belong to their owners.</p>
<h3 style="color:#fff">No placement guarantee</h3>
<p>We do not guarantee jobs, interviews, salary outcomes or exam passes. Career results depend on individual effort, market conditions and employer decisions.</p>
<h3 style="color:#fff">External links &amp; services</h3>
<p>Payments (Razorpay), ebooks (Gumroad) and email (Resend) are provided by third parties under their own terms. We are not responsible for their availability or conduct.</p>
<h3 style="color:#fff">Opinions &amp; testimonials</h3>
<p>Views expressed in articles and community stories are personal opinions, not professional advice.</p>
<h3 style="color:#fff">Contact</h3>
<p>hello@grcwithgaurav.com</p>
</div>
{% endblock %}"""

for name, content in [("privacy.html", privacy), ("terms.html", terms), ("disclaimer.html", disclaimer)]:
    open(os.path.join(tdir, name), "w", encoding="utf-8").write(content)
    print("[TEMPLATE]", name)

sr = [x for x in glob.glob("**/site_routes.py", recursive=True) if not any(t in x for t in skip)][0]
r = open(sr, encoding="utf-8").read()
added = 0
routes = '''@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@router.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer_page(request: Request):
    return templates.TemplateResponse("disclaimer.html", {"request": request})

'''
if '"/privacy"' not in r:
    anchor = '@router.get("/refund-policy", response_class=HTMLResponse)'
    if anchor not in r:
        anchor = '@router.get("/admin-leads", response_class=HTMLResponse)'
    r = r.replace(anchor, routes + anchor)
    added = 1
    print("[ROUTE] /privacy /terms /disclaimer added")

# Footer href normalization (kill 404 variants)
bh = [x for x in glob.glob("**/base.html", recursive=True) if not any(t in x for t in skip)][0]
b = open(bh, encoding="utf-8").read()
orig = b
for old, new in [('href="/privacy-policy"', 'href="/privacy"'), ('href="/privacy.html"', 'href="/privacy"'),
                 ('href="/terms-of-service"', 'href="/terms"'), ('href="/terms.html"', 'href="/terms"'), ('href="/tos"', 'href="/terms"'),
                 ('href="/disclaimer.html"', 'href="/disclaimer"')]:
    b = b.replace(old, new)
if 'href="/privacy"' not in b:
    b = b.replace('<a href="/refund-policy">Refunds</a>', '<a href="/refund-policy">Refunds</a>\n            <a href="/privacy">Privacy</a>\n            <a href="/terms">Terms</a>\n            <a href="/disclaimer">Disclaimer</a>')
if b != orig:
    print("[FOOTER] links normalized")
open(bh, "w", encoding="utf-8").write(b)
if added:
    open(sr, "w", encoding="utf-8").write(r)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Compliance: privacy, terms, disclaimer pages + footer link fixes"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
