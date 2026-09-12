import subprocess, re

print("=== DIAGNOSING CURRENT STATE ===\n")

# === FIX 2: Check /learn and /resources templates ===
print("1. /learn template:")
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
print(f"   Extends base.html: {'{% extends' in learn and 'base.html' in learn}")
print(f"   Has block canonical: {'{% block canonical' in learn}")
print(f"   Has og:image: {'og:image' in learn}")
print(f"   Size: {len(learn)} chars")

print("\n2. /resources template:")
res = open("backend/templates/resources.html", encoding="utf-8").read()
print(f"   Extends base.html: {'{% extends' in res and 'base.html' in res}")
print(f"   Has block canonical: {'{% block canonical' in res}")
print(f"   Has og:image: {'og:image' in res}")
print(f"   Size: {len(res)} chars")

print("\n3. Article canonical:")
art = open("backend/templates/learn/article.html", encoding="utf-8").read()
idx = art.find("{% block canonical %}")
if idx >= 0:
    print(f"   Current: {art[idx:idx+120]}")

print("\n4. Homepage pricing:")
idx_html = open("backend/templates/index.html", encoding="utf-8").read()
print(f"   Has 'Cancel anytime': {'Cancel anytime' in idx_html}")
print(f"   Has 499: {'499' in idx_html}")

print("\n5. App freemium modal:")
app = open("frontend/app.html", encoding="utf-8").read()
print(f"   Has 'Cancel anytime': {'Cancel anytime' in app}")
print(f"   Has 'Upgrade to Pro': {'Upgrade to Pro' in app}")

print("\n=== APPLYING ALL 5 FIXES ===\n")

# === FIX 4: Remove trailing slash from article canonical ===
old_canonical = "{% block canonical %}{{ base_url }}/learn/{{ article.slug }}/{% endblock %}"
new_canonical = "{% block canonical %}{{ base_url }}/learn/{{ article.slug }}{% endblock %}"
if old_canonical in art:
    art = art.replace(old_canonical, new_canonical)
    open("backend/templates/learn/article.html", "w", encoding="utf-8").write(art)
    print("[FIX 4] ✅ Removed trailing slash from article canonical")
else:
    print("[FIX 4] ⚠️  Canonical pattern not matched")

# === FIX 3: De-dupe ebook content from /resources ===
# Find the book loop and replace with link to /books
if "{% for b in books %}" in res:
    idx = res.find("{% for b in books %}")
    end_idx = res.find("{% endfor %}", idx)
    if end_idx > idx:
        old_section = res[idx:end_idx+12]
        # Find the parent div that contains the loop
        parent_start = res.rfind('<div', 0, idx)
        parent_end = res.find('</div>', end_idx) + 6
        if parent_start >= 0 and parent_end > 0:
            old_block = res[parent_start:parent_end]
            new_block = '<div class="card" style="padding:1.5rem;margin-top:1.5rem"><h3 style="margin-top:0">Ebooks & Playbooks</h3><p style="color:var(--muted);margin:.5rem 0 1rem">Three practical playbooks for GRC and AI in security careers.</p><a href="/books" class="btn-primary" style="display:inline-block">See All Books &rarr;</a></div>'
            res = res.replace(old_block, new_block)
            open("backend/templates/resources.html", "w", encoding="utf-8").write(res)
            print("[FIX 3] ✅ Replaced book loop on /resources with link to /books")
        else:
            print("[FIX 3] ⚠️  Could not find parent div for book loop")
else:
    print("[FIX 3] ⚠️  No book loop found in resources.html")

# === FIX 2: Add proper meta blocks to /learn and /resources ===
# For /learn
if "{% block canonical %}" not in learn:
    # Add meta blocks after {% block content %}
    content_idx = learn.find("{% block content %}")
    if content_idx > 0:
        meta_block = """{% block canonical %}{{ base_url }}/learn{% endblock %}
{% block head %}
<meta property="og:image" content="{{ base_url }}/static/og-default.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="{{ base_url }}/learn">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{{ base_url }}/static/og-default.jpg">
<meta name="twitter:title" content="Learn Cybersecurity, GRC & ISO 27001 | GRCWithGaurav">
<meta name="twitter:description" content="Practical, human-reviewed guides on ISO 27001, GRC, SOC careers and AI in cybersecurity - each linked to free tools and CyberVerse AI.">
{% endblock %}
"""
        learn = learn[:content_idx] + meta_block + learn[content_idx:]
        open("backend/templates/learn/index.html", "w", encoding="utf-8").write(learn)
        print("[FIX 2] ✅ Added meta blocks to /learn")
else:
    print("[FIX 2] ⚠️  /learn already has canonical block")

# For /resources
if "{% block canonical %}" not in res:
    content_idx = res.find("{% block content %}")
    if content_idx > 0:
        meta_block = """{% block canonical %}{{ base_url }}/resources{% endblock %}
{% block head %}
<meta property="og:image" content="{{ base_url }}/static/og-default.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="{{ base_url }}/resources">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{{ base_url }}/static/og-default.jpg">
<meta name="twitter:title" content="Free Cybersecurity Resources & Starter Kit | GRCWithGaurav">
<meta name="twitter:description" content="Free cybersecurity starter kit: ISO 27001 risk register, audit checklist, GRC interview questions, career roadmap and resume template - plus ebooks.">
{% endblock %}
"""
        res = res[:content_idx] + meta_block + res[content_idx:]
        open("backend/templates/resources.html", "w", encoding="utf-8").write(res)
        print("[FIX 2] ✅ Added meta blocks to /resources")
else:
    print("[FIX 2] ⚠️  /resources already has canonical block")

# === FIX 1: Update pricing table on homepage ===
# Premium differentiator: "1:1 career strategy session with Gaurav + all future playbooks"
old_pricing = '''<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:750px;margin:0 auto">
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
        </div>'''

new_pricing = '''<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;max-width:950px;margin:0 auto">
            <div style="padding:1.5rem;background:#0a0a0a;border:1px solid #333;border-radius:12px">
                <h4 style="color:#fff;margin-top:0">Free</h4>
                <p style="color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem">Get started, no card needed</p>
                <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem;margin:0">
                    <li>3 mock interviews / month</li>
                    <li>Basic feedback (pass/fail + summary)</li>
                    <li>GRC &amp; SOC fundamentals</li>
                </ul>
                <a href="/app.html" class="btn-secondary" style="display:block;text-align:center;margin-top:1.5rem">Start Free</a>
            </div>
            <div style="padding:1.5rem;background:#0a0a0a;border:2px solid var(--accent);border-radius:12px;position:relative">
                <span style="position:absolute;top:-12px;right:16px;background:var(--accent);color:#000;font-size:.75rem;font-weight:700;padding:.2rem .7rem;border-radius:10px">MOST POPULAR</span>
                <h4 style="color:var(--accent);margin-top:0">Pro — 499</h4>
                <p style="color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem">One-time payment, lifetime access</p>
                <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem;margin:0">
                    <li>Unlimited interviews</li>
                    <li>Detailed scoring + improvement plan</li>
                    <li>All topic tracks</li>
                    <li>Streak tracking + analytics</li>
                    <li>Shareable verified certificate</li>
                    <li>Priority AI response speed</li>
                </ul>
                <a href="/app.html" class="btn-primary" style="display:block;text-align:center;margin-top:1.5rem">Get Pro — 499</a>
            </div>
            <div style="padding:1.5rem;background:#0a0a0a;border:2px solid #8b5cf6;border-radius:12px;position:relative">
                <span style="position:absolute;top:-12px;right:16px;background:linear-gradient(135deg,#8b5cf6,#00ffcc);color:#000;font-size:.75rem;font-weight:700;padding:.2rem .7rem;border-radius:10px">PREMIUM</span>
                <h4 style="color:#8b5cf6;margin-top:0">Premium — 999</h4>
                <p style="color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem">One-time payment, lifetime access</p>
                <ul style="color:#c9c9c9;font-size:.85rem;line-height:1.7;padding-left:1.2rem;margin:0">
                    <li>Everything in Pro, plus:</li>
                    <li>1:1 career strategy session (60 min with Gaurav)</li>
                    <li>All future playbooks included</li>
                    <li>Priority email support</li>
                    <li>Resume review + LinkedIn optimization</li>
                </ul>
                <a href="/app.html" class="btn-primary" style="display:block;text-align:center;margin-top:1.5rem;background:linear-gradient(135deg,#8b5cf6,#00ffcc);color:#000">Get Premium — 999</a>
            </div>
        </div>
        <p style="text-align:center;color:var(--muted);font-size:.85rem;margin-top:1.5rem;margin-bottom:0">7-day money-back guarantee. One-time payment, lifetime access.</p>'''

if old_pricing in idx_html:
    idx_html = idx_html.replace(old_pricing, new_pricing)
    # Also update the subheading
    old_sub = "CyberVerse AI gives you real mock interviews with AI feedback — no credit card needed to start."
    new_sub = "CyberVerse AI gives you real mock interviews with AI feedback. Free to start, one-time payment to unlock everything — no subscriptions."
    idx_html = idx_html.replace(old_sub, new_sub)
    open("backend/templates/index.html", "w", encoding="utf-8").write(idx_html)
    print("[FIX 1] ✅ Updated homepage pricing table (3 tiers, correct pricing)")
else:
    print("[FIX 1] ⚠️  Pricing table pattern not matched")

# === FIX 1 (continued): Update freemium modal in app.html ===
old_modal = '''<h3 style="color:#fff;margin:0 0 1rem">You've used all 3 free interviews this month 🎯</h3>
    <p style="color:var(--muted);line-height:1.6;margin:0 0 1.5rem">You're improving — your last score was <span id="freemium-score" style="color:var(--accent);font-weight:600">72</span>%. Unlock unlimited interviews, detailed feedback on every answer, and a shareable certificate when you're ready.</p>
    <div style="display:flex;gap:.75rem">
      <button class="btn-primary" onclick="window.location.href='/billing/checkout/pro'" style="flex:1">Upgrade to Pro</button>
      <button class="btn-secondary" onclick="document.getElementById('freemium-modal').style.display='none'" style="flex:1">Remind me next month</button>
    </div>'''

new_modal = '''<h3 style="color:#fff;margin:0 0 1rem">You've used all 3 free interviews this month 🎯</h3>
    <p style="color:var(--muted);line-height:1.6;margin:0 0 1.5rem">You're improving — your last score was <span id="freemium-score" style="color:var(--accent);font-weight:600">72</span>%. Unlock unlimited interviews, detailed feedback on every answer, and a shareable certificate when you're ready.</p>
    <div style="display:flex;gap:.75rem">
      <button class="btn-primary" onclick="window.location.href='/billing/checkout/pro'" style="flex:1">Upgrade to Pro — 499</button>
      <button class="btn-secondary" onclick="document.getElementById('freemium-modal').style.display='none'" style="flex:1">Remind me next month</button>
    </div>
    <p style="text-align:center;color:var(--muted);font-size:.75rem;margin-top:.75rem;margin-bottom:0">One-time payment, lifetime access. 7-day money-back guarantee.</p>'''

if old_modal in app:
    app = app.replace(old_modal, new_modal)
    # Also update the soft nudge
    old_nudge = '<p style="color:var(--muted);font-size:.85rem;margin:0 0 .75rem;line-height:1.5">Pro members get unlimited practice + detailed scoring.</p>'
    new_nudge = '<p style="color:var(--muted);font-size:.85rem;margin:0 0 .75rem;line-height:1.5">Pro (499 lifetime) gives unlimited practice + detailed scoring.</p>'
    app = app.replace(old_nudge, new_nudge)
    open("frontend/app.html", "w", encoding="utf-8").write(app)
    print("[FIX 1] ✅ Updated app.html freemium modal + nudge with pricing")
else:
    print("[FIX 1] ⚠️  Modal pattern not matched")

# === COMMIT + PUSH ===
print("\n=== COMMITTING CHANGES ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: pricing table (3 tiers), template consolidation, article canonical, resources de-dupe"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
