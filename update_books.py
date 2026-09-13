import subprocess

new_books = '''{% extends "base.html" %}
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
  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">Breaking Into GRC: A Career-Changer's Guide</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">No coding background. No IT degree. A real 90-day transition path into GRC &mdash; resume rewrites, 5 portfolio projects, and the interview playbook, built from a real career change.</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">$9</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra &middot; 49-page PDF</span>
   </p>
   <a href="https://malhotra72.gumroad.com/l/GRC" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>

  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">Cybersecurity Prompt Library: 80+ Battle-Tested Prompts</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">80+ ready-to-use AI prompts for policy drafting, risk assessment, incident response, and AI governance &mdash; aligned with ISO 27001, NIST, and the EU AI Act.</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">$9</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra &middot; 52-page PDF</span>
   </p>
   <a href="https://malhotra72.gumroad.com/l/Promptlibrary" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>

  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">AI Workflows for Cybersecurity Professionals &mdash; Practitioner Playbook</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">6 end-to-end AI workflows for SOC triage, threat intel, GRC/compliance, offensive security, and reporting &mdash; with guardrail checklists. AI drafts, you validate.</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">$9</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra &middot; 24-page PDF</span>
   </p>
   <a href="https://malhotra72.gumroad.com/l/cyberhustle" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>

  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">The AI Governance Playbook (2nd Edition)</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">NIST AI RMF, EU AI Act, and ISO/IEC 42001 mapped to the ISO 27001 program you already run &mdash; plus 7 done-for-you templates and new agentic AI governance guidance.</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">$9</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra &middot; 66-page PDF + 7 templates</span>
   </p>
   <a href="https://malhotra72.gumroad.com/l/wxhxoo" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>

  <div class="card" style="padding:1.8rem">
   <h2 style="color:#fff;margin-top:0;font-size:1.5rem">ISO 27001:2022 Gap Analysis &amp; Certification Toolkit</h2>
   <p style="color:#c9c9c9;line-height:1.7;margin:.6rem 0 1rem">The consultant-grade Excel toolkit: all 93 Annex A controls, a self-calculating compliance dashboard, SoA template, risk register, and 12-month certification roadmap.</p>
   <p style="margin:.4rem 0 .8rem">
    <span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.2rem .8rem;font-size:.85rem">$9</span>
    <span style="color:var(--muted);font-size:.85rem;margin-left:.4rem">by Gaurav Malhotra &middot; Excel dashboard + bonuses</span>
   </p>
   <a href="https://malhotra72.gumroad.com/l/Gapanalysis" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get It on Gumroad &rarr;</a>
  </div>
 </div>

 <div class="card" style="padding:2rem;margin-top:2.5rem;text-align:center;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:2px solid var(--accent);position:relative">
  <span style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--accent);color:#000;font-size:.75rem;font-weight:700;padding:.2rem .9rem;border-radius:10px;white-space:nowrap">BEST VALUE &mdash; SAVE $10</span>
  <h2 style="color:#fff;margin-top:.5rem">The Complete Cybersecurity Career Bundle</h2>
  <p style="color:var(--muted);max-width:640px;margin:0 auto 1rem">All 5 playbooks in one package &mdash; Breaking Into GRC, the Prompt Library, AI Workflows, the AI Governance Playbook, and the ISO 27001 Gap Analysis Toolkit. Everything, one price.</p>
  <p style="margin:0 0 1.2rem"><span style="color:var(--muted);text-decoration:line-through;font-size:1.05rem">$45</span><span style="color:#fff;font-weight:700;font-size:1.5rem;margin-left:.6rem">$35</span></p>
  <a href="https://malhotra72.gumroad.com/l/Cybersecuritybundle" target="_blank" rel="noopener" class="btn-primary" style="display:inline-block">Get the Bundle &mdash; $35 &rarr;</a>
 </div>

 <div class="card" style="padding:2rem;margin-top:2rem;text-align:center;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent)">
  <h2 style="color:#fff;margin-top:0">Better together: CyberVerse AI + the playbooks</h2>
  <p style="color:var(--muted);max-width:600px;margin:0 auto 1rem">Upgrade to CyberVerse AI Pro this month and get any book free.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Upgrade & Claim Your Free Book &rarr;</a>
 </div>

 <div class="card" style="padding:1.5rem;margin-top:2rem;text-align:center;background:#111;border:1px solid #222">
  <p style="color:var(--muted);margin:0">All books come with Gumroad's standard refund policy. If it's not useful to you, you get your money back &mdash; no hard feelings.</p>
 </div>
</div>
{% endblock %}
'''

open("backend/templates/books.html", "w", encoding="utf-8").write(new_books)
print("[REWRITTEN] books.html with 5 books + $35 bundle card")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Books: 5 individual products + $35 bundle card with real Gumroad links"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
