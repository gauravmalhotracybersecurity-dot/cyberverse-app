import os, subprocess

os.makedirs("backend/templates/tools", exist_ok=True)

# ---------- 1. TOOLS INDEX PAGE ----------
tools_index = """{% extends "base.html" %}
{% block title %}Free Cybersecurity & GRC Tools | GRCWithGaurav{% endblock %}
{% block description %}Free, practical cybersecurity and GRC tools: ISO 27001 risk calculator, CVSS calculator, ATS resume checker and more. No signup required.{% endblock %}
{% block content %}
<div style="max-width:1100px;margin:0 auto;padding:2rem">
 <h1 style="color:#fff;text-align:center">Free Cybersecurity & GRC Tools</h1>
 <p style="color:var(--muted);text-align:center;max-width:700px;margin:0 auto 2.5rem">Practical, no-signup tools for security and GRC professionals. Results are informational and do not replace professional audits or certification body reviews.</p>
 <div class="grid-3">
  <div class="card"><h3>ISO 27001 Risk Calculator</h3><p>Likelihood x Impact scoring, live risk register and CSV export.</p><a href="/tools/iso-risk-calculator">Use Tool &rarr;</a></div>
  <div class="card"><h3>CVSS Calculator</h3><p>Score vulnerabilities using the CVSS v3.1 standard.</p><span style="color:var(--muted)">Coming soon</span></div>
  <div class="card"><h3>ISO 27001 Gap Assessment</h3><p>Check your compliance posture against key requirements.</p><span style="color:var(--muted)">Coming soon</span></div>
  <div class="card"><h3>Risk Register Generator</h3><p>Build, document and export a complete risk register.</p><span style="color:var(--muted)">Coming soon</span></div>
  <div class="card"><h3>Resume ATS Checker</h3><p>See if your cybersecurity resume passes the bots.</p><a href="/app.html">Try in CyberVerse AI &rarr;</a></div>
  <div class="card"><h3>Career Roadmap Generator</h3><p>Get a 6-month SOC / GRC roadmap.</p><a href="/app.html">Try in CyberVerse AI &rarr;</a></div>
 </div>
</div>
{% endblock %}"""
open("backend/templates/tools/index.html", "w", encoding="utf-8").write(tools_index)
print("[CREATED] tools/index.html")

# ---------- 2. ISO 27001 RISK CALCULATOR ----------
calc = """{% extends "base.html" %}
{% block title %}Free ISO 27001 Risk Calculator | GRCWithGaurav{% endblock %}
{% block description %}Calculate ISO 27001 risk scores (Likelihood x Impact), document controls and treatment plans, and export your risk register to CSV. Free, no signup.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/iso-risk-calculator/{% endblock %}
{% block head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "ISO 27001 Risk Calculator",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" },
  "description": "Free ISO 27001 risk calculator with configurable thresholds, risk register and CSV export."
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
 input,select{width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box}
 .score-box{margin-top:1rem;padding:1rem;border-radius:10px;background:#151515;border:1px solid #333;display:flex;gap:1rem;align-items:center}
 .score-num{font-size:2rem;font-weight:800;color:#fff}
 .badge{padding:.3rem .8rem;border-radius:20px;font-weight:700;font-size:.85rem;color:#000}
 table{width:100%;border-collapse:collapse;margin-top:1.5rem;font-size:.85rem}
 th,td{padding:.5rem;border-bottom:1px solid #222;text-align:left;color:var(--text);vertical-align:top}
 th{color:var(--muted)}
 .row-actions button{background:none;border:none;color:var(--accent);cursor:pointer;font-size:.85rem}
 .btn-row{display:flex;gap:.8rem;margin-top:1rem;flex-wrap:wrap}
 .notice{background:#101a17;border:1px solid #1d4034;color:#9fdcc3;padding:.8rem 1rem;border-radius:10px;font-size:.85rem;margin:1rem 0}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / ISO 27001 Risk Calculator</div>
 <h1>ISO 27001 Risk Calculator</h1>
 <p style="color:var(--muted);max-width:780px">Score each risk as <strong style="color:#fff">Likelihood &times; Impact</strong>, document existing controls and treatment options, then export a CSV risk register. Risk-level thresholds are configurable in one place (RISK_CONFIG).</p>
 <div class="notice">&#9888;&#65039; This tool is for informational purposes only and does not replace a professional risk assessment, audit, or certification body review.</div>

 <div class="card" style="padding:1.5rem">
  <div class="tool-grid">
   <div><label>Asset *</label><input id="f-asset" placeholder="e.g. Customer database"></div>
   <div><label>Threat *</label><input id="f-threat" placeholder="e.g. Ransomware / data exfiltration"></div>
   <div><label>Vulnerability *</label><input id="f-vuln" placeholder="e.g. Unpatched OS, no MFA"></div>
   <div><label>Existing controls</label><input id="f-controls" placeholder="e.g. EDR, daily backups"></div>
   <div><label>Likelihood (1-5)</label><select id="f-like"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div>
   <div><label>Impact (1-5)</label><select id="f-imp"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div>
   <div><label>Risk owner</label><input id="f-owner" placeholder="e.g. CISO / IT Manager"></div>
   <div><label>Treatment option</label><select id="f-treat"><option>Mitigate</option><option>Avoid</option><option>Transfer</option><option>Accept</option></select></div>
  </div>
  <div class="score-box">
    <div style="color:var(--muted)">Risk Score</div>
    <div class="score-num" id="live-score">&ndash;</div>
    <span class="badge" id="live-badge" style="background:#333;color:#aaa">Set L &amp; I</span>
  </div>
  <div class="btn-row">
    <button class="btn-primary" id="btn-add">+ Add Risk to Register</button>
    <button class="btn-secondary" id="btn-export">&#11123; Export CSV</button>
    <button class="btn-secondary" id="btn-clear">Clear All</button>
  </div>
 </div>

 <table id="risk-table" style="display:none"><thead><tr><th>#</th><th>Asset</th><th>Threat</th><th>Vulnerability</th><th>L</th><th>I</th><th>Score</th><th>Level</th><th>Controls</th><th>Owner</th><th>Treatment</th><th></th></tr></thead><tbody></tbody></table>

 <div class="cta-card">
   <h2 style="color:#fff;margin:0 0 .5rem" id="cta-title">Want AI-powered remediation recommendations?</h2>
   <p style="color:var(--muted)" id="cta-sub">CyberVerse AI turns your risk register into a prioritized treatment plan with control recommendations mapped to ISO 27001 Annex A.</p>
   <a href="/app.html" class="btn-primary" style="display:inline-block">Analyse with CyberVerse AI &rarr;</a>
 </div>

 <section style="margin-top:3rem;max-width:840px">
   <h2 style="color:#fff">How the ISO 27001 risk score works</h2>
   <p style="color:var(--muted)">ISO/IEC 27001 requires organizations to identify, analyse and evaluate information security risks, then select appropriate treatment options and controls (Annex A). This calculator uses the common quantitative shortcut <strong style="color:#fff">Risk Score = Likelihood &times; Impact</strong> on a 5&times;5 scale. Default bands: 1&ndash;4 Low, 5&ndash;9 Medium, 10&ndash;16 High, 17&ndash;25 Critical. Documenting existing controls and owners turns a raw score into an auditable risk register entry.</p>
   <h2 style="color:#fff">Related tools</h2>
   <p style="color:var(--muted)"><a href="/tools">All free tools &rarr;</a> &middot; CVSS Calculator (coming soon) &middot; ISO 27001 Gap Assessment (coming soon)</p>
 </section>
</div>

<script>
var RISK_CONFIG = { levels: [
  { max: 4,  label: "Low",      color: "#22c55e" },
  { max: 9,  label: "Medium",   color: "#eab308" },
  { max: 16, label: "High",     color: "#f97316" },
  { max: 25, label: "Critical", color: "#ef4444" }
]};
function levelFor(s){ for (var i=0;i<RISK_CONFIG.levels.length;i++){ if (s<=RISK_CONFIG.levels[i].max) return RISK_CONFIG.levels[i]; } return RISK_CONFIG.levels[RISK_CONFIG.levels.length-1]; }
var risks = []; try { risks = JSON.parse(localStorage.getItem("cv_risks") || "[]"); } catch(e){}
var editIdx = -1;
function save(){ localStorage.setItem("cv_risks", JSON.stringify(risks)); }
function val(id){ return document.getElementById(id).value; }
function esc(s){ var d=document.createElement("div"); d.textContent=(s==null?"":s); return d.innerHTML; }
function live(){ var s=parseInt(val("f-like"),10)*parseInt(val("f-imp"),10); var lv=levelFor(s); document.getElementById("live-score").textContent=s; var b=document.getElementById("live-badge"); b.textContent=lv.label; b.style.background=lv.color; b.style.color="#000"; }
document.getElementById("f-like").onchange=live; document.getElementById("f-imp").onchange=live;
function render(){
  var tb=document.querySelector("#risk-table tbody"); tb.innerHTML="";
  document.getElementById("risk-table").style.display = risks.length ? "table" : "none";
  var hc=0;
  risks.forEach(function(r,i){
    var lv=levelFor(r.score); if(lv.label==="High"||lv.label==="Critical") hc++;
    var tr=document.createElement("tr");
    tr.innerHTML="<td>"+(i+1)+"</td><td>"+esc(r.asset)+"</td><td>"+esc(r.threat)+"</td><td>"+esc(r.vuln)+"</td><td>"+r.l+"</td><td>"+r.i+"</td><td><strong>"+r.score+"</strong></td><td><span class='badge' style='background:"+lv.color+"'>"+lv.label+"</span></td><td>"+esc(r.controls)+"</td><td>"+esc(r.owner)+"</td><td>"+esc(r.treat)+"</td><td class='row-actions'><button onclick='editR("+i+")'>Edit</button> <button onclick='delR("+i+")'>Del</button></td>";
    tb.appendChild(tr);
  });
  if (hc>0) document.getElementById("cta-title").textContent = "Your assessment identified " + hc + " high/critical risk" + (hc>1?"s":"") + ".";
}
document.getElementById("btn-add").onclick=function(){
  if(!val("f-asset")||!val("f-threat")||!val("f-vuln")){ alert("Asset, Threat and Vulnerability are required."); return; }
  var r={asset:val("f-asset"),threat:val("f-threat"),vuln:val("f-vuln"),controls:val("f-controls"),l:parseInt(val("f-like"),10),i:parseInt(val("f-imp"),10),owner:val("f-owner"),treat:val("f-treat")};
  r.score=r.l*r.i;
  if(editIdx>-1){ risks[editIdx]=r; editIdx=-1; document.getElementById("btn-add").textContent="+ Add Risk to Register"; } else { risks.push(r); }
  save(); render();
};
window.editR=function(i){ var r=risks[i]; editIdx=i;
  document.getElementById("f-asset").value=r.asset; document.getElementById("f-threat").value=r.threat; document.getElementById("f-vuln").value=r.vuln; document.getElementById("f-controls").value=r.controls; document.getElementById("f-like").value=r.l; document.getElementById("f-imp").value=r.i; document.getElementById("f-owner").value=r.owner; document.getElementById("f-treat").value=r.treat;
  live(); document.getElementById("btn-add").textContent="Save Changes"; window.scrollTo(0,0);
};
window.delR=function(i){ risks.splice(i,1); save(); render(); };
document.getElementById("btn-clear").onclick=function(){ if(confirm("Delete all risks?")){ risks=[]; save(); render(); } };
document.getElementById("btn-export").onclick=function(){
  if(!risks.length){ alert("Add at least one risk first."); return; }
  var rows=[["#","Asset","Threat","Vulnerability","Likelihood","Impact","Risk Score","Risk Level","Existing Controls","Owner","Treatment"]];
  risks.forEach(function(r,i){ var lv=levelFor(r.score); rows.push([i+1,r.asset,r.threat,r.vuln,r.l,r.i,r.score,lv.label,r.controls,r.owner,r.treat]); });
  var csv=rows.map(function(row){ return row.map(function(c){ c=String(c==null?"":c); return '"'+c.replace(/"/g,'""')+'"'; }).join(","); }).join("\\n");
  var a=document.createElement("a"); a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"})); a.download="iso27001-risk-register.csv"; a.click();
};
render(); live();
</script>
{% endblock %}"""
open("backend/templates/tools/iso_risk_calculator.html", "w", encoding="utf-8").write(calc)
print("[CREATED] tools/iso_risk_calculator.html")

# ---------- 3. SITE ROUTES ----------
routes = """from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/tools", response_class=HTMLResponse)
async def tools_index(request: Request):
    return templates.TemplateResponse("tools/index.html", {"request": request})

@router.get("/tools/iso-risk-calculator", response_class=HTMLResponse)
async def iso_risk_calculator(request: Request):
    return templates.TemplateResponse("tools/iso_risk_calculator.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
@router.get("/careers", response_class=HTMLResponse)
@router.get("/resources", response_class=HTMLResponse)
async def placeholders(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
"""
open("backend/routers/site_routes.py", "w", encoding="utf-8").write(routes)
print("[UPDATED] site_routes.py with /tools + calculator routes")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 3: ISO 27001 Risk Calculator + tools index"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
