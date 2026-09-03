import os, subprocess

# ---------- 1. CVSS v3.1 CALCULATOR TEMPLATE ----------
cvss = """{% extends "base.html" %}
{% block title %}Free CVSS v3.1 Calculator | GRCWithGaurav{% endblock %}
{% block description %}Calculate CVSS v3.1 base scores using the official FIRST formula. Live vector string, exploitability and impact subscores, and plain-English explanations. Free.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/cvss-calculator/{% endblock %}
{% block head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "CVSS v3.1 Calculator",
  "applicationCategory": "SecurityApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" },
  "description": "Free CVSS v3.1 base score calculator using the official FIRST scoring formula."
}
</script>
<style>
 .wrap{max-width:1100px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 h1{color:#fff}
 .tool-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
 @media(max-width:800px){.tool-grid{grid-template-columns:1fr}}
 label{display:block;color:var(--muted);font-size:.85rem;margin:.6rem 0 .25rem}
 select{width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box}
 .score-box{margin-top:1.2rem;padding:1.2rem;border-radius:10px;background:#151515;border:1px solid #333;display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap}
 .score-num{font-size:2.4rem;font-weight:800;color:#fff}
 .badge{padding:.35rem .9rem;border-radius:20px;font-weight:700;font-size:.9rem;color:#000}
 .vector{margin-top:1rem;padding:.8rem 1rem;border-radius:8px;background:#0d0d0d;border:1px dashed #333;color:var(--accent);font-family:monospace;font-size:.85rem;word-break:break-all}
 .sub{color:var(--muted);font-size:.85rem}
 .btn-row{display:flex;gap:.8rem;margin-top:1rem;flex-wrap:wrap}
 .notice{background:#101a17;border:1px solid #1d4034;color:#9fdcc3;padding:.8rem 1rem;border-radius:10px;font-size:.85rem;margin:1rem 0}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / CVSS Calculator</div>
 <h1>CVSS Calculator <span style="color:var(--accent);font-size:1rem;vertical-align:middle">implements CVSS v3.1</span></h1>
 <p style="color:var(--muted);max-width:780px">This calculator implements the official <strong style="color:#fff">CVSS v3.1 Base Score formula</strong> as published by FIRST.org (the same math used by NVD). Select the eight base metrics and the score, severity, subscores and vector string update live.</p>
 <div class="notice">&#9888;&#65039; CVSS scores are a severity rating, not a risk rating. They do not account for your environment, exposure or business context &mdash; use them inside a broader risk assessment.</div>

 <div class="card" style="padding:1.5rem">
  <div class="tool-grid">
   <div><label>Attack Vector (AV)</label><select id="m-av"><option value="0.85|N">Network (N)</option><option value="0.62|A">Adjacent Network (A)</option><option value="0.55|L">Local (L)</option><option value="0.20|P">Physical (P)</option></select></div>
   <div><label>Attack Complexity (AC)</label><select id="m-ac"><option value="0.77|L">Low (L)</option><option value="0.44|H">High (H)</option></select></div>
   <div><label>Privileges Required (PR)</label><select id="m-pr"><option value="N">None (N)</option><option value="L">Low (L)</option><option value="H">High (H)</option></select></div>
   <div><label>User Interaction (UI)</label><select id="m-ui"><option value="0.85|N">None (N)</option><option value="0.62|R">Required (R)</option></select></div>
   <div><label>Scope (S)</label><select id="m-s"><option value="U">Unchanged (U)</option><option value="C">Changed (C)</option></select></div>
   <div><label>Confidentiality (C)</label><select id="m-c"><option value="0.56|H">High (H)</option><option value="0.22|L">Low (L)</option><option value="0|N">None (N)</option></select></div>
   <div><label>Integrity (I)</label><select id="m-i"><option value="0.56|H">High (H)</option><option value="0.22|L">Low (L)</option><option value="0|N">None (N)</option></select></div>
   <div><label>Availability (A)</label><select id="m-a"><option value="0.56|H">High (H)</option><option value="0.22|L">Low (L)</option><option value="0|N">None (N)</option></select></div>
  </div>

  <div class="score-box">
    <div><div class="sub">Base Score</div><div class="score-num" id="out-score">0.0</div></div>
    <span class="badge" id="out-sev" style="background:#333;color:#aaa">None</span>
    <div><div class="sub">Exploitability</div><strong id="out-expl" style="color:#fff">0.00</strong></div>
    <div><div class="sub">Impact</div><strong id="out-imp" style="color:#fff">0.00</strong></div>
  </div>
  <div class="vector" id="out-vector">CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H</div>
  <div class="btn-row">
    <button class="btn-primary" id="btn-copy">Copy Vector String</button>
  </div>
 </div>

 <section style="margin-top:3rem;max-width:840px">
   <h2 style="color:#fff">How the score is calculated (CVSS v3.1)</h2>
   <p style="color:var(--muted)">Impact Sub-Score (ISS) = 1 &minus; [(1&minus;C) &times; (1&minus;I) &times; (1&minus;A)]. If Scope Unchanged: Impact = 6.42 &times; ISS; if Scope Changed: Impact = 7.52 &times; (ISS &minus; 0.029) &minus; 3.25 &times; (ISS &minus; 0.02)^15. Exploitability = 8.22 &times; AV &times; AC &times; PR &times; UI. Base Score = Roundup(min(Impact + Exploitability, 10)), or Roundup(min(1.08 &times; (Impact + Exploitability), 10)) when Scope is Changed. Privileges Required is weighted differently when Scope is Changed, per the specification. Severity bands: 0.0 None, 0.1&ndash;3.9 Low, 4.0&ndash;6.9 Medium, 7.0&ndash;8.9 High, 9.0&ndash;10.0 Critical.</p>
   <h2 style="color:#fff">Related tools</h2>
   <p style="color:var(--muted)"><a href="/tools/iso-risk-calculator">ISO 27001 Risk Calculator &rarr;</a> &middot; <a href="/tools">All free tools &rarr;</a></p>
 </section>

 <div class="cta-card">
   <h2 style="color:#fff;margin:0 0 .5rem">Interviewers love CVSS questions.</h2>
   <p style="color:var(--muted)">Can you explain why Scope Changed raises the score? Practice answering out loud &mdash; the AI grades you like a hiring manager.</p>
   <a href="/app.html" class="btn-primary" style="display:inline-block">Practice with CyberVerse AI &rarr;</a>
 </div>
</div>

<script>
function val(id){ return document.getElementById(id).value; }
function roundup(x){ return Math.ceil(x*10)/10; }
function sev(s){ if(s<=0) return ["None","#333","#aaa"]; if(s<4) return ["Low","#22c55e","#000"]; if(s<7) return ["Medium","#eab308","#000"]; if(s<9) return ["High","#f97316","#000"]; return ["Critical","#ef4444","#000"]; }
function compute(){
  var av=val("m-av").split("|"), ac=val("m-ac").split("|"), ui=val("m-ui").split("|");
  var AV=parseFloat(av[0]), AC=parseFloat(ac[0]), UI=parseFloat(ui[0]);
  var S=val("m-s");
  var prMap = (S==="C") ? {N:0.85,L:0.68,H:0.50} : {N:0.85,L:0.62,H:0.27};
  var PR=prMap[val("m-pr")];
  var C=parseFloat(val("m-c").split("|")[0]), I=parseFloat(val("m-i").split("|")[0]), A=parseFloat(val("m-a").split("|")[0]);
  var ISS = 1-((1-C)*(1-I)*(1-A));
  var impact = (S==="U") ? 6.42*ISS : 7.52*(ISS-0.029)-3.25*Math.pow(ISS-0.02,15);
  var expl = 8.22*AV*AC*PR*UI;
  var base = 0;
  if (impact>0){ base = (S==="U") ? roundup(Math.min(impact+expl,10)) : roundup(Math.min(1.08*(impact+expl),10)); }
  var sv = sev(base);
  document.getElementById("out-score").textContent = base.toFixed(1);
  var b=document.getElementById("out-sev"); b.textContent=sv[0]; b.style.background=sv[1]; b.style.color=sv[2];
  document.getElementById("out-expl").textContent = expl.toFixed(2);
  document.getElementById("out-imp").textContent = Math.max(impact,0).toFixed(2);
  document.getElementById("out-vector").textContent = "CVSS:3.1/AV:"+av[1]+"/AC:"+ac[1]+"/PR:"+val("m-pr")+"/UI:"+ui[1]+"/S:"+S+"/C:"+val("m-c").split("|")[1]+"/I:"+val("m-i").split("|")[1]+"/A:"+val("m-a").split("|")[1];
}
["m-av","m-ac","m-pr","m-ui","m-s","m-c","m-i","m-a"].forEach(function(id){ document.getElementById(id).onchange=compute; });
document.getElementById("btn-copy").onclick=function(){
  var t=document.getElementById("out-vector").textContent;
  if(navigator.clipboard){ navigator.clipboard.writeText(t); }
  this.textContent="Copied!"; var el=this; setTimeout(function(){ el.textContent="Copy Vector String"; },1500);
};
compute();
</script>
{% endblock %}"""
open("backend/templates/tools/cvss_calculator.html", "w", encoding="utf-8").write(cvss)
print("[CREATED] tools/cvss_calculator.html")

# ---------- 2. UPDATE TOOLS INDEX (CVSS card -> live) ----------
ti = "backend/templates/tools/index.html"
c = open(ti, encoding="utf-8").read()
old = '<div class="card"><h3>CVSS Calculator</h3><p>Score vulnerabilities using the CVSS v3.1 standard.</p><span style="color:var(--muted)">Coming soon</span></div>'
new = '<div class="card"><h3>CVSS Calculator</h3><p>Score vulnerabilities using the official CVSS v3.1 formula.</p><a href="/tools/cvss-calculator">Use Tool &rarr;</a></div>'
if old in c:
    open(ti, "w", encoding="utf-8").write(c.replace(old, new))
    print("[UPDATED] tools index: CVSS card now live")

# ---------- 3. ADD ROUTE ----------
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if "cvss-calculator" not in r:
    anchor = '@router.get("/learn", response_class=HTMLResponse)'
    route = '''@router.get("/tools/cvss-calculator", response_class=HTMLResponse)
async def cvss_calculator(request: Request):
    return templates.TemplateResponse("tools/cvss_calculator.html", {"request": request})

'''
    r = r.replace(anchor, route + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[UPDATED] site_routes.py: /tools/cvss-calculator route added")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 3: CVSS v3.1 calculator with official FIRST formula"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
