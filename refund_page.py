import glob, subprocess
skip = ("venv", "node_modules", ".git")

tpl = """{% extends "base.html" %}
{% block title %}Refund & Cancellation Policy | GRCWithGaurav{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Refund &amp; Cancellation Policy</h1>
 <p style="color:var(--muted)">Last updated: 8 September 2026</p>
 <h3 style="color:#fff;margin-top:1.5rem">1. Digital delivery</h3>
 <p style="color:#c9c9c9">All CyberVerse AI plans (Pro, Premium) and ebooks are digital products. Access is activated automatically within seconds of successful payment. No physical shipping applies.</p>
 <h3 style="color:#fff;margin-top:1.5rem">2. Cancellation</h3>
 <p style="color:#c9c9c9">Plans are one-time lifetime purchases with no auto-renewal, so there are no recurring charges to cancel. You may stop using the service at any time.</p>
 <h3 style="color:#fff;margin-top:1.5rem">3. Refund eligibility</h3>
 <ul style="color:#c9c9c9;line-height:1.8">
  <li>Access not activated within 24 hours of payment despite a successful transaction.</li>
  <li>Duplicate or accidental double payment (the duplicate is refunded in full).</li>
  <li>Material defect: paid features remain unusable for 7 consecutive days after a verified support attempt.</li>
  <li>Refund requests raised within 7 days of purchase for unused plans.</li>
 </ul>
 <h3 style="color:#fff;margin-top:1.5rem">4. Non-refundable</h3>
 <ul style="color:#c9c9c9;line-height:1.8">
  <li>Plans actively used (interviews completed, resume reviews consumed) beyond 7 days.</li>
  <li>Downloaded ebooks or generated certificates already consumed.</li>
  <li>Failed payments (no money was captured).</li>
 </ul>
 <h3 style="color:#fff;margin-top:1.5rem">5. How to request</h3>
 <p style="color:#c9c9c9">Email your payment ID and registered email to <strong>hello@grcwithgaurav.com</strong>. Approved refunds are returned to the original payment method within 5-7 business days.</p>
 <h3 style="color:#fff;margin-top:1.5rem">6. Contact</h3>
 <p style="color:#c9c9c9">GRC With Gaurav (CyberVerse AI), India. Grievances: hello@grcwithgaurav.com.</p>
</div>
{% endblock %}"""

import os
tdir = None
for root, dirs, files in os.walk("."):
    if any(t in root for t in skip): continue
    if os.path.basename(root) == "templates" and "backend" in root.replace("\\", "/"):
        tdir = root; break
open(os.path.join(tdir, "refunds.html"), "w", encoding="utf-8").write(tpl)
print("[TEMPLATE] refunds.html created")

sr = [x for x in glob.glob("**/site_routes.py", recursive=True) if not any(t in x for t in skip)][0]
r = open(sr, encoding="utf-8").read()
if '"/refund-policy"' not in r:
    anchor = '@router.get("/admin-leads", response_class=HTMLResponse)'
    block = '''@router.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy_page(request: Request):
    return templates.TemplateResponse("refunds.html", {"request": request})

'''
    r = r.replace(anchor, block + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[ROUTE] /refund-policy added")

bh = [x for x in glob.glob("**/base.html", recursive=True) if not any(t in x for t in skip)][0]
b = open(bh, encoding="utf-8").read()
if "/refund-policy" not in b:
    b = b.replace('<a href="/privacy">Privacy</a>', '<a href="/privacy">Privacy</a>\n            <a href="/refund-policy">Refunds</a>')
    open(bh, "w", encoding="utf-8").write(b)
    print("[FOOTER] Refunds link added")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Compliance: refund & cancellation policy page for Razorpay live review"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
