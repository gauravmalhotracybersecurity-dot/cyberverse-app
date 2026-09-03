import subprocess

# ---------- 1. BACKEND ENDPOINTS (append to analytics_routes) ----------
endpoints = '''


@router.post("/b2b/lead")
def b2b_lead(payload: dict, db: Session = Depends(get_db)):
    import re as _re
    from sqlalchemy import text as _text
    from datetime import datetime as _dt
    p = payload or {}
    if p.get("website"):
        return {"ok": True}  # honeypot triggered - pretend success, save nothing
    name = str(p.get("name", "") or "").strip()[:200]
    email = str(p.get("email", "") or "").strip()[:200]
    company = str(p.get("company", "") or "").strip()[:200]
    if not name or not company or not _re.match(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$", email):
        return {"ok": False, "error": "Name, work email and company are required."}
    size = str(p.get("size", "") or "")[:50]
    industry = str(p.get("industry", "") or "")[:100]
    status = str(p.get("status", "") or "")[:100]
    requirement = str(p.get("requirement", "") or "")[:2000]
    timeline = str(p.get("timeline", "") or "")[:50]
    try:
        db.execute(_text("CREATE TABLE IF NOT EXISTS b2b_leads (name TEXT, email TEXT, company TEXT, size TEXT, industry TEXT, status TEXT, requirement TEXT, timeline TEXT, created_at TEXT)"))
        db.execute(_text("INSERT INTO b2b_leads (name,email,company,size,industry,status,requirement,timeline,created_at) VALUES (:n,:e,:c,:s,:i,:t,:r,:tl,:ca)"),
                   {"n": name, "e": email, "c": company, "s": size, "i": industry, "t": status, "r": requirement, "tl": timeline, "ca": _dt.utcnow().isoformat()})
        db.commit()
    except Exception:
        return {"ok": False, "error": "Could not save your request. Please try again."}
    return {"ok": True}


@router.get("/b2b/leads")
def b2b_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    try:
        rows = db.execute(_text("SELECT name,email,company,size,industry,status,requirement,timeline,created_at FROM b2b_leads ORDER BY created_at DESC LIMIT 200")).fetchall()
    except Exception:
        rows = []
    return [{"name": r[0], "email": r[1], "company": r[2], "size": r[3], "industry": r[4], "status": r[5], "requirement": r[6], "timeline": r[7], "created_at": r[8]} for r in rows]
'''
ar = "backend/routers/analytics_routes.py"
c = open(ar, encoding="utf-8").read()
if "def b2b_lead" not in c:
    open(ar, "w", encoding="utf-8").write(c + endpoints)
    print("[BACKEND] /api/analytics/b2b/lead + /b2b/leads added")

# ---------- 2. B2B PAGE TEMPLATE ----------
b2b = """{% extends "base.html" %}
{% block title %}Free GRC Assessment for Businesses | GRCWithGaurav{% endblock %}
{% block description %}Get a free, scoped GRC assessment: current posture, priority gaps and a 90-day roadmap for ISO 27001, SOC 2 and security governance.{% endblock %}
{% block content %}
<div style="max-width:760px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff">Need help with ISO 27001 or GRC?</h1>
 <p style="color:var(--muted)">Tell us where you are and where you need to be. You get a scoped assessment: current posture, priority gaps and a prioritized 90-day roadmap. No obligation, no spam.</p>
 <form id="b2b-form" class="card" style="padding:1.5rem;margin-top:1.5rem">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem" class="fg">
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Name *</label><input id="b-name" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box"></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Work email *</label><input id="b-email" type="email" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box"></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Company *</label><input id="b-company" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box"></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Company size</label><select id="b-size" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff"><option>1-10</option><option>11-50</option><option>51-200</option><option>201-1000</option><option>1000+</option></select></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Industry</label><select id="b-industry" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff"><option>SaaS</option><option>Fintech</option><option>Healthcare</option><option>Manufacturing</option><option>Consulting</option><option>Other</option></select></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Current compliance status</label><select id="b-status" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff"><option>No formal program</option><option>In progress</option><option>ISO 27001 certified</option><option>SOC 2 certified</option><option>Other</option></select></div>
   <div><label style="display:block;color:var(--muted);font-size:.85rem;margin:.4rem 0 .25rem">Target timeline</label><select id="b-timeline" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff"><option>ASAP</option><option>3 months</option><option>6 months</option><option>12 months</option><option>Exploring</option></select></div>
  </div>
  <label style="display:block;color:var(--muted);font-size:.85rem;margin:.8rem 0 .25rem">What do you need help with?</label>
  <textarea id="b-req" style="width:100%;min-height:110px;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box" placeholder="e.g. We need ISO 27001 certification before a Q2 enterprise deal..."></textarea>
  <input type="text" id="b-website" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
  <div style="margin-top:1rem"><button type="submit" class="btn-primary" id="b-submit">Get a Free GRC Assessment</button></div>
  <p id="b-msg" style="margin-top:.8rem;font-size:.88rem"></p>
  <p style="color:#666;font-size:.75rem;margin-top:.8rem">We use these details only to respond to your request. See our Privacy Policy.</p>
 </form>
</div>
<script>
document.getElementById("b2b-form").onsubmit = function(e){
  e.preventDefault();
  var msg = document.getElementById("b-msg");
  var body = { name: document.getElementById("b-name").value, email: document.getElementById("b-email").value, company: document.getElementById("b-company").value, size: document.getElementById("b-size").value, industry: document.getElementById("b-industry").value, status: document.getElementById("b-status").value, timeline: document.getElementById("b-timeline").value, requirement: document.getElementById("b-req").value, website: document.getElementById("b-website").value };
  fetch("/api/analytics/b2b/lead", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
  .then(function(r){ return r.json(); })
  .then(function(d){
    if (d.ok) { msg.style.color = "#22c55e"; msg.textContent = "Request received. We will reply within 1 business day."; document.getElementById("b2b-form").reset(); }
    else { msg.style.color = "#ef4444"; msg.textContent = d.error || "Something went wrong. Please try again."; }
  })
  .catch(function(){ msg.style.color = "#ef4444"; msg.textContent = "Network error. Please try again."; });
};
</script>
{% endblock %}"""
open("backend/templates/b2b.html", "w", encoding="utf-8").write(b2b)
print("[CREATED] b2b.html")

# ---------- 3. ROUTE + HOMEPAGE SECTION ----------
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if '"/b2b"' not in r:
    anchor = '@router.get("/careers", response_class=HTMLResponse)'
    route = '''@router.get("/b2b", response_class=HTMLResponse)
async def b2b_page(request: Request):
    return templates.TemplateResponse("b2b.html", {"request": request})

'''
    r = r.replace(anchor, route + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[ROUTE] /b2b added")

hp = "backend/templates/index.html"
h = open(hp, encoding="utf-8").read()
if "Free GRC Assessment" not in h:
    biz = """
<section class="section">
    <h2>Need help with ISO 27001 or GRC?</h2>
    <div class="card" style="text-align:center; max-width:800px; margin:0 auto;">
        <h3 style="color:#fff;">Get a Free GRC Assessment</h3>
        <p>For businesses: a scoped review of your current posture, priority gaps and a 90-day roadmap - no obligation.</p>
        <a href="/b2b" class="btn-primary" style="display:inline-block; margin-top:1rem;">Get a Free GRC Assessment</a>
    </div>
</section>
"""
    idx = h.rfind("{% endblock %}")
    h = h[:idx] + biz + h[idx:]
    open(hp, "w", encoding="utf-8").write(h)
    print("[HOMEPAGE] B2B section added")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 5: B2B lead gen funnel + secure leads storage"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
