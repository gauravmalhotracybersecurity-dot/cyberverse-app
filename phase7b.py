import subprocess

# ================= 1. INCIDENT SEVERITY CALCULATOR =================
inc = r"""{% extends "base.html" %}
{% block title %}Free Incident Severity Calculator | GRCWithGaurav{% endblock %}
{% block description %}Classify security incidents into SEV-1 to SEV-4 using impact, scope, business criticality and containment status - with response tracks and notification flags.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/incident-severity-calculator/{% endblock %}
{% block head %}
<style>
 .wrap{max-width:900px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 label{display:block;color:var(--muted);font-size:.85rem;margin:.6rem 0 .25rem}
 select{width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box}
 .grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
 @media(max-width:800px){.grid2{grid-template-columns:1fr}}
 .sev-box{margin-top:1.2rem;padding:1.4rem;border-radius:12px;background:#151515;border:1px solid #333}
 .sev-num{font-size:2.2rem;font-weight:800}
 .notice{background:#101a17;border:1px solid #1d4034;color:#9fdcc3;padding:.8rem 1rem;border-radius:10px;font-size:.85rem;margin:1rem 0}
 .flag{margin-top:.8rem;padding:.7rem 1rem;border-radius:8px;background:#2a1215;border:1px solid #7f1d1d;color:#fca5a5;font-size:.88rem;display:none}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / Incident Severity Calculator</div>
 <h1>Incident Severity Calculator</h1>
 <p style="color:var(--muted)">Answer five questions to classify the incident (SEV-1 to SEV-4), get the right response track, and see whether regulatory notification needs a legal review.</p>
 <div class="notice">&#9888;&#65039; Informational guidance only. Always follow your organization's incident response plan and legal advice.</div>
 <div class="card" style="padding:1.5rem">
  <div class="grid2">
   <div><label>Incident type</label><select id="i-type"><option value="3">Data breach / exfiltration</option><option value="3">Ransomware</option><option value="2">DDoS / availability attack</option><option value="2">Phishing campaign</option><option value="2">Malware on host</option><option value="2">Insider misuse</option><option value="1">Misconfiguration exposure</option><option value="1">Other / unknown</option></select></div>
   <div><label>Data / systems affected</label><select id="i-data"><option value="3">PII / customer data</option><option value="3">Credentials / secrets</option><option value="3">Critical production systems</option><option value="2">Internal systems only</option><option value="1">Single endpoint</option><option value="0">None identified</option></select></div>
   <div><label>Scope</label><select id="i-scope"><option value="3">Enterprise-wide / multiple sites</option><option value="2">Multiple hosts</option><option value="1">Single host</option><option value="1">Single account</option></select></div>
   <div><label>Business impact</label><select id="i-biz"><option value="3">Revenue stopped / regulatory exposure</option><option value="2">Major operational degradation</option><option value="1">Minor impact</option><option value="0">None observed yet</option></select></div>
   <div><label>Containment status</label><select id="i-cont"><option value="3">Actively spreading</option><option value="2">Not contained</option><option value="1">Partially contained</option><option value="0">Fully contained</option></select></div>
  </div>
 </div>
 <div class="sev-box">
   <div style="color:var(--muted)">Classification</div>
   <div class="sev-num" id="out-sev" style="color:#22c55e">SEV-4</div>
   <p id="out-track" style="color:#c9c9c9;margin:.6rem 0 0"></p>
   <div class="flag" id="out-flag">&#9878;&#65039; Personal data or regulatory exposure indicated - open the notification review: many regimes (e.g. GDPR 72h, India DPDP "as soon as practicable", sectoral rules) require timely regulator and affected-party notification. Involve legal now.</div>
 </div>
 <div class="cta-card">
  <h2 style="color:#fff;margin:0 0 .5rem">Can you walk an interviewer through this incident?</h2>
  <p style="color:var(--muted)">CyberVerse AI runs incident-response mock interviews: containment, evidence, communication - graded out loud.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Practice IR with CyberVerse AI &rarr;</a>
 </div>
</div>
<script>
function v(id){ return parseInt(document.getElementById(id).value,10); }
function compute(){
  var s=v("i-type")+v("i-data")+v("i-scope")+v("i-biz")+v("i-cont");
  var el=document.getElementById("out-sev"), tr=document.getElementById("out-track");
  var sev,col,track;
  if(s>=11){ sev="SEV-1"; col="#ef4444"; track="Critical. Activate the IR plan NOW: war room, executive + legal + comms engaged, evidence preservation started, external forensics on standby."; }
  else if(s>=8){ sev="SEV-2"; col="#f97316"; track="High. Respond within hours: assigned incident commander, containment actions, stakeholder updates every few hours."; }
  else if(s>=4){ sev="SEV-3"; col="#eab308"; track="Medium. Respond within 1 business day: ticketed response, containment + monitoring, standard reporting."; }
  else { sev="SEV-4"; col="#22c55e"; track="Low. Log and monitor: handle in normal queue, document for trend analysis."; }
  el.textContent=sev+" ("+s+"/15)"; el.style.color=col; tr.textContent=track;
  document.getElementById("out-flag").style.display=(v("i-data")===3||v("i-biz")===3)?"block":"none";
}
["i-type","i-data","i-scope","i-biz","i-cont"].forEach(function(id){ document.getElementById(id).onchange=compute; });
compute();
</script>
{% endblock %}"""
open("backend/templates/tools/incident_severity_calculator.html", "w", encoding="utf-8").write(inc)
print("[CREATED] incident_severity_calculator.html")

# ================= 2. VENDOR RISK ASSESSMENT =================
ven = r"""{% extends "base.html" %}
{% block title %}Free Vendor Risk Assessment | GRCWithGaurav{% endblock %}
{% block description %}Score third-party vendors across data, access, certifications, encryption, incident response, continuity, privacy and subprocessors - with contract fixes for every red flag.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/vendor-risk-assessment/{% endblock %}
{% block head %}
<style>
 .wrap{max-width:900px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 label{display:block;color:var(--muted);font-size:.85rem;margin:.6rem 0 .25rem}
 select{width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box}
 .grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
 @media(max-width:800px){.grid2{grid-template-columns:1fr}}
 .sev-box{margin-top:1.2rem;padding:1.4rem;border-radius:12px;background:#151515;border:1px solid #333}
 .sev-num{font-size:2.2rem;font-weight:800}
 .finding{border-left:3px solid #ef4444;background:#151515;padding:.6rem 1rem;border-radius:6px;margin-bottom:.5rem;font-size:.88rem}
 .finding .act{color:var(--muted);display:block;margin-top:.25rem}
 .btn-row{display:flex;gap:.8rem;margin-top:1rem;flex-wrap:wrap}
 .notice{background:#101a17;border:1px solid #1d4034;color:#9fdcc3;padding:.8rem 1rem;border-radius:10px;font-size:.85rem;margin:1rem 0}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / Vendor Risk Assessment</div>
 <h1>Vendor Risk Assessment</h1>
 <p style="color:var(--muted)">Answer nine questions about a third-party vendor. You get an inherent risk rating plus the exact contract clauses to fix every red flag.</p>
 <div class="notice">&#9888;&#65039; This rates inherent risk for guidance. Final vendor decisions require due diligence, legal review and your procurement policy.</div>
 <div class="card" style="padding:1.5rem">
  <div class="grid2">
   <div><label>Data handled</label><select id="v-data"><option value="0">No sensitive data</option><option value="1">Internal data only</option><option value="2">PII / customer / confidential</option></select></div>
   <div><label>Service criticality</label><select id="v-crit"><option value="0">Nice-to-have</option><option value="1">Important</option><option value="2">Business-critical</option></select></div>
   <div><label>Access to your environment</label><select id="v-access"><option value="0">No system access</option><option value="1">Limited / scoped access</option><option value="2">Admin or broad access</option></select></div>
   <div><label>Security certifications</label><select id="v-cert"><option value="0">ISO 27001 or SOC 2 Type II</option><option value="1">SOC 1 / self-attestation only</option><option value="2">None</option></select></div>
   <div><label>Encryption</label><select id="v-enc"><option value="0">In transit + at rest</option><option value="1">In transit only</option><option value="2">None / unknown</option></select></div>
   <div><label>Incident response</label><select id="v-ir"><option value="0">Defined IR + breach notification SLA</option><option value="1">Informal process</option><option value="2">None described</option></select></div>
   <div><label>Business continuity</label><select id="v-bc"><option value="0">Tested BCP/DR</option><option value="1">BCP exists, untested</option><option value="2">None</option></select></div>
   <div><label>Privacy posture</label><select id="v-priv"><option value="0">DPA signed + subprocessor list public</option><option value="1">DPA only</option><option value="2">Neither</option></select></div>
   <div><label>Subprocessors</label><select id="v-sub"><option value="0">Disclosed and governed</option><option value="1">Partially disclosed</option><option value="2">Unknown</option></select></div>
  </div>
 </div>
 <div class="sev-box">
   <div style="color:var(--muted)">Inherent Risk Rating</div>
   <div class="sev-num" id="out-rate" style="color:#22c55e">Low</div>
   <p id="out-sum" style="color:#c9c9c9;margin:.6rem 0 0"></p>
 </div>
 <h2 style="color:#fff;margin-top:2rem">Red flags &amp; contract fixes</h2>
 <div id="flags"><p style="color:var(--muted)">No red flags - strong vendor posture.</p></div>
 <div class="btn-row"><button class="btn-primary" id="btn-copy">Copy Summary</button></div>
 <div class="cta-card">
  <h2 style="color:#fff;margin:0 0 .5rem">Managing a whole vendor portfolio?</h2>
  <p style="color:var(--muted)">CyberVerse AI helps you build the vendor risk register, review schedules and audit-right language at scale.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Analyse with CyberVerse AI &rarr;</a>
 </div>
</div>
<script>
var Q=[
 {id:"v-data",n:"Data handled",fix:"Limit shared data to the minimum; add data classification and handling terms."},
 {id:"v-crit",n:"Service criticality",fix:"Require higher availability SLAs and exit/transition assistance clauses."},
 {id:"v-access",n:"Environment access",fix:"Enforce least privilege, SSO + MFA, and quarterly access reviews."},
 {id:"v-cert",n:"Security certifications",fix:"Request independent attestation (ISO 27001 / SOC 2) or a right-to-audit clause."},
 {id:"v-enc",n:"Encryption",fix:"Require encryption in transit and at rest within the DPA."},
 {id:"v-ir",n:"Incident response",fix:"Contract a breach notification SLA (24-72h) and cooperation obligations."},
 {id:"v-bc",n:"Business continuity",fix:"Ask for BCP/DR test evidence or a recent test report."},
 {id:"v-priv",n:"Privacy posture",fix:"Sign a DPA and require a current subprocessor list before go-live."},
 {id:"v-sub",n:"Subprocessors",fix:"Require subprocessor disclosure and flow-down of security obligations."}
];
function compute(){
  var s=0, flags=[];
  Q.forEach(function(q){ var val=parseInt(document.getElementById(q.id).value,10); s+=val; if(val===2) flags.push(q); });
  var el=document.getElementById("out-rate"), col, lbl;
  if(s<=4){ lbl="Low"; col="#22c55e"; } else if(s<=9){ lbl="Medium"; col="#eab308"; } else if(s<=14){ lbl="High"; col="#f97316"; } else { lbl="Critical"; col="#ef4444"; }
  el.textContent=lbl+" ("+s+"/18)"; el.style.color=col;
  document.getElementById("out-sum").textContent = flags.length ? flags.length+" red flag area"+(flags.length>1?"s":"")+" need contract treatment before signing." : "No red flags detected. Standard contract terms are sufficient.";
  var f=document.getElementById("flags");
  if(flags.length){ f.innerHTML=""; flags.forEach(function(q){ var d=document.createElement("div"); d.className="finding"; d.innerHTML="<strong>"+q.n+"</strong><span class='act'>Contract fix: "+q.fix+"</span>"; f.appendChild(d); }); }
  else f.innerHTML="<p style='color:var(--muted)'>No red flags - strong vendor posture.</p>";
  window._ven={s:s,lbl:lbl,flags:flags};
}
Q.forEach(function(q){ document.getElementById(q.id).onchange=compute; });
document.getElementById("btn-copy").onclick=function(){
  var r=window._ven; var lines=["Vendor Risk Assessment - GRCWithGaurav","Rating: "+r.lbl+" ("+r.s+"/18)","","Red flags & contract fixes:"];
  if(r.flags.length){ r.flags.forEach(function(q){ lines.push("- "+q.n+": "+q.fix); }); } else lines.push("- none");
  navigator.clipboard.writeText(lines.join("\n"));
  this.textContent="Copied!"; var el=this; setTimeout(function(){el.textContent="Copy Summary"},1500);
};
compute();
</script>
{% endblock %}"""
open("backend/templates/tools/vendor_risk_assessment.html", "w", encoding="utf-8").write(ven)
print("[CREATED] vendor_risk_assessment.html")

# ================= 3. INDEX CARDS + ROUTES =================
ti = "backend/templates/tools/index.html"
c = open(ti, encoding="utf-8").read()
c = c.replace('<div class="card"><h3>Incident Severity Calculator</h3><p>Classify incidents and pick the right response track.</p><span style="color:var(--muted)">Coming soon</span></div>',
              '<div class="card"><h3>Incident Severity Calculator</h3><p>SEV-1 to SEV-4 classification with response tracks.</p><a href="/tools/incident-severity-calculator">Use Tool &rarr;</a></div>')
c = c.replace('<div class="card"><h3>Vendor Risk Assessment</h3><p>Questionnaire-based third-party risk rating.</p><span style="color:var(--muted)">Coming soon</span></div>',
              '<div class="card"><h3>Vendor Risk Assessment</h3><p>9-point third-party scoring with contract fixes.</p><a href="/tools/vendor-risk-assessment">Use Tool &rarr;</a></div>')
open(ti, "w", encoding="utf-8").write(c)
print("[UPDATED] tools index - all 10 tools live")

sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if "incident-severity-calculator" not in r:
    anchor = '@router.get("/b2b", response_class=HTMLResponse)'
    routes = '''@router.get("/tools/incident-severity-calculator", response_class=HTMLResponse)
async def incident_severity_calculator(request: Request):
    return templates.TemplateResponse("tools/incident_severity_calculator.html", {"request": request})

@router.get("/tools/vendor-risk-assessment", response_class=HTMLResponse)
async def vendor_risk_assessment(request: Request):
    return templates.TemplateResponse("tools/vendor_risk_assessment.html", {"request": request})

'''
    r = r.replace(anchor, routes + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[UPDATED] routes added")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 7 complete: Incident Severity + Vendor Risk - all 10 tools live"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. ALL 10 TOOLS LIVE.")
