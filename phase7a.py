import subprocess

# ================= 1. SECURITY POLICY GENERATOR =================
policy_gen = r"""{% extends "base.html" %}
{% block title %}Free Security Policy Generator | GRCWithGaurav{% endblock %}
{% block description %}Generate professional drafts for Information Security, Password, Acceptable Use, and Incident Response policies. Free, no signup.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/security-policy-generator/{% endblock %}
{% block head %}
<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Security Policy Generator","applicationCategory":"BusinessApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"INR"}}</script>
<style>
 .wrap{max-width:900px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 label{display:block;color:var(--muted);font-size:.85rem;margin:.6rem 0 .25rem}
 input,select{width:100%;padding:.6rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box}
 .notice{background:#3a1c1c;border:1px solid #5c2626;color:#fca5a5;padding:.8rem 1rem;border-radius:10px;font-size:.85rem;margin:1rem 0}
 .doc-box{margin-top:1.5rem;padding:2rem;border-radius:10px;background:#fff;color:#000;font-family: 'Times New Roman', Times, serif;line-height:1.6;max-height:600px;overflow-y:auto;display:none}
 .doc-box h1{color:#000;font-size:1.5rem;text-align:center;border-bottom:2px solid #000;padding-bottom:.5rem}
 .doc-box h2{color:#000;font-size:1.1rem;margin-top:1.5rem;border-bottom:1px solid #ccc;padding-bottom:.2rem}
 .btn-row{display:flex;gap:.8rem;margin-top:1rem;flex-wrap:wrap}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / Security Policy Generator</div>
 <h1>Security Policy Generator</h1>
 <p style="color:var(--muted)">Generate professional, ISO 27001-aligned policy drafts for your organization. Fill in the details below to create a baseline document.</p>
 <div class="notice">&#9888;&#65039; <strong>Important Disclaimer:</strong> Generated policies are drafts for guidance only. They require organizational, legal, and security management review and approval before formal adoption.</div>

 <div class="card" style="padding:1.5rem">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
   <div><label>Company Name *</label><input id="p-company" placeholder="e.g. Acme Corp"></div>
   <div><label>Effective Date</label><input id="p-date" type="date"></div>
   <div style="grid-column:span 2"><label>Policy Type *</label>
    <select id="p-type">
     <option value="infosec">Information Security Policy (Overarching)</option>
     <option value="password">Password & Authentication Policy</option>
     <option value="acceptable">Acceptable Use Policy (AUP)</option>
     <option value="incident">Incident Response Policy</option>
     <option value="vendor">Vendor & Third-Party Risk Policy</option>
    </select>
   </div>
  </div>
  <div class="btn-row"><button class="btn-primary" id="btn-gen">Generate Policy Draft</button></div>
 </div>

 <div class="doc-box" id="doc-out"></div>
 <div class="btn-row" id="doc-actions" style="display:none">
  <button class="btn-primary" id="btn-copy">Copy to Clipboard</button>
  <button class="btn-secondary" id="btn-print">Print / Save PDF</button>
 </div>

 <div class="cta-card">
  <h2 style="color:#fff;margin:0 0 .5rem">Policies are just paper without enforcement.</h2>
  <p style="color:var(--muted)">CyberVerse AI helps you map these policies to technical controls and tests your team on them via mock audits.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Practice with CyberVerse AI &rarr;</a>
 </div>
</div>

<script>
var TEMPLATES = {
 infosec: `<h1>Information Security Policy</h1><p><strong>Company:</strong> {{COMPANY}} | <strong>Effective Date:</strong> {{DATE}}</p><h2>1. Purpose</h2><p>The purpose of this policy is to protect {{COMPANY}}'s information assets from all threats, internal or external, deliberate or accidental. This policy ensures the confidentiality, integrity, and availability of information.</p><h2>2. Scope</h2><p>This policy applies to all employees, contractors, and third parties accessing {{COMPANY}} systems and data.</p><h2>3. Roles and Responsibilities</h2><p>Management is responsible for supporting this policy. The Information Security Manager is responsible for its implementation and maintenance. All users must comply with the policy.</p><h2>4. Core Principles</h2><ul><li><strong>Confidentiality:</strong> Data is only accessible to authorized individuals.</li><li><strong>Integrity:</strong> Data is accurate and protected from unauthorized modification.</li><li><strong>Availability:</strong> Systems and data are accessible when needed.</li></ul><h2>5. Compliance & Enforcement</h2><p>Violations of this policy may result in disciplinary action. This policy is reviewed annually.</p>`,
 password: `<h1>Password & Authentication Policy</h1><p><strong>Company:</strong> {{COMPANY}} | <strong>Effective Date:</strong> {{DATE}}</p><h2>1. Purpose</h2><p>To establish standards for the creation, use, and protection of passwords and authentication mechanisms.</p><h2>2. Requirements</h2><ul><li>Passwords must be at least 12 characters long.</li><li>Must include a mix of uppercase, lowercase, numbers, and symbols.</li><li>Multi-Factor Authentication (MFA) is mandatory for all remote access and privileged accounts.</li><li>Passwords must not be shared or written down in plain text.</li></ul><h2>3. System Administration</h2><p>Systems must enforce password complexity and lock accounts after 5 failed attempts.</p>`,
 acceptable: `<h1>Acceptable Use Policy (AUP)</h1><p><strong>Company:</strong> {{COMPANY}} | <strong>Effective Date:</strong> {{DATE}}</p><h2>1. Purpose</h2><p>To outline the acceptable use of computer equipment and networks at {{COMPANY}}.</p><h2>2. General Use</h2><ul><li>Company systems are for business purposes. Incidental personal use is permitted if it does not interfere with work.</li><li>Users must not install unauthorized software.</li><li>Users must not attempt to bypass security controls.</li></ul><h2>3. Prohibited Activities</h2><p>Accessing illegal content, harassing others, or using company resources for personal financial gain is strictly prohibited.</p>`,
 incident: `<h1>Incident Response Policy</h1><p><strong>Company:</strong> {{COMPANY}} | <strong>Effective Date:</strong> {{DATE}}</p><h2>1. Purpose</h2><p>To ensure a consistent, effective approach to handling security incidents.</p><h2>2. Reporting</h2><p>All employees must report suspected security incidents to the IT/Security team immediately. Do not attempt to investigate or "fix" the issue yourself.</p><h2>3. Phases of Response</h2><ul><li><strong>Preparation:</strong> Maintaining tools and training.</li><li><strong>Identification:</strong> Determining if an event is an incident.</li><li><strong>Containment:</strong> Limiting the damage.</li><li><strong>Eradication & Recovery:</strong> Removing the threat and restoring systems.</li><li><strong>Lessons Learned:</strong> Post-incident review.</li></ul>`,
 vendor: `<h1>Vendor & Third-Party Risk Policy</h1><p><strong>Company:</strong> {{COMPANY}} | <strong>Effective Date:</strong> {{DATE}}</p><h2>1. Purpose</h2><p>To manage the risks associated with third-party vendors who access {{COMPANY}} data or systems.</p><h2>2. Assessment</h2><p>All new vendors must undergo a security assessment before contract signing. Critical vendors must be reassessed annually.</p><h2>3. Contracts</h2><p>Contracts must include "Right to Audit" clauses, data breach notification requirements (within 24 hours), and data return/destruction terms.</p>`
};
document.getElementById("btn-gen").onclick=function(){
  var co=document.getElementById("p-company").value;
  if(!co){alert("Please enter a Company Name."); return;}
  var dt=document.getElementById("p-date").value || new Date().toISOString().split("T")[0];
  var tp=document.getElementById("p-type").value;
  var html=TEMPLATES[tp].replace(/\{\{COMPANY\}\}/g, co).replace(/\{\{DATE\}\}/g, dt);
  document.getElementById("doc-out").innerHTML=html;
  document.getElementById("doc-out").style.display="block";
  document.getElementById("doc-actions").style.display="flex";
  document.getElementById("doc-out").scrollIntoView({behavior:"smooth"});
};
document.getElementById("btn-copy").onclick=function(){
  var text=document.getElementById("doc-out").innerText;
  navigator.clipboard.writeText(text);
  this.textContent="Copied!"; var el=this; setTimeout(function(){el.textContent="Copy to Clipboard"},1500);
};
document.getElementById("btn-print").onclick=function(){window.print();};
</script>
{% endblock %}"""
open("backend/templates/tools/security_policy_generator.html", "w", encoding="utf-8").write(policy_gen)
print("[CREATED] tools/security_policy_generator.html")

# ================= 2. ISO 27001:2022 CONTROL FINDER =================
control_finder = r"""{% extends "base.html" %}
{% block title %}ISO 27001:2022 Annex A Control Finder | GRCWithGaurav{% endblock %}
{% block description %}Search and filter the 93 controls of the ISO 27001:2022 Annex A across the 4 themes: Organizational, People, Physical, and Technological.{% endblock %}
{% block canonical %}https://grcwithgaurav.com/tools/iso27001-control-finder/{% endblock %}
{% block head %}
<style>
 .wrap{max-width:1000px;margin:0 auto;padding:2rem}
 .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
 .crumbs a{color:var(--muted)}
 input{width:100%;padding:.8rem;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;box-sizing:border-box;font-size:1rem;margin-bottom:1rem}
 .filters{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem}
 .filters button{padding:.5rem 1rem;border-radius:20px;border:1px solid #333;background:#111;color:#fff;cursor:pointer;font-size:.85rem}
 .filters button.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:700}
 .ctrl{background:#111;border:1px solid #222;border-radius:8px;padding:1rem;margin-bottom:.5rem}
 .ctrl-id{color:var(--accent);font-weight:700;font-family:monospace}
 .ctrl-theme{font-size:.75rem;background:#222;color:#aaa;padding:.2rem .5rem;border-radius:10px;margin-left:.5rem}
 .cta-card{margin-top:2.5rem;padding:2rem;border-radius:14px;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);text-align:center}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <div class="crumbs"><a href="/">Home</a> / <a href="/tools">Tools</a> / ISO 27001 Control Finder</div>
 <h1>ISO 27001:2022 Annex A Control Finder</h1>
 <p style="color:var(--muted)">The 2022 revision consolidated Annex A into 93 controls across 4 themes. Search by keyword or filter by theme to find the exact control you need for your Statement of Applicability (SoA).</p>
 <input id="search" placeholder="Search controls (e.g. 'encryption', 'MFA', 'vendor')...">
 <div class="filters">
  <button class="active" data-theme="all">All (93)</button>
  <button data-theme="Org">Organizational (37)</button>
  <button data-theme="People">People (8)</button>
  <button data-theme="Phys">Physical (14)</button>
  <button data-theme="Tech">Technological (34)</button>
 </div>
 <div id="list"></div>

 <div class="cta-card">
  <h2 style="color:#fff;margin:0 0 .5rem">Struggling to justify exclusions in your SoA?</h2>
  <p style="color:var(--muted)">CyberVerse AI helps you draft the justification for every control in your Statement of Applicability based on your risk register.</p>
  <a href="/app.html" class="btn-primary" style="display:inline-block">Build SoA with CyberVerse AI &rarr;</a>
 </div>
</div>
<script>
var C=[
// Organizational
{id:"5.1",t:"Org",n:"Policies for information security"},{id:"5.2",t:"Org",n:"Establishing roles and responsibilities"},{id:"5.3",t:"Org",n:"Segregation of duties"},{id:"5.4",t:"Org",n:"Management responsibilities"},{id:"5.5",t:"Org",n:"Contact with authorities"},{id:"5.6",t:"Org",n:"Contact with special interest groups"},{id:"5.7",t:"Org",n:"Threat intelligence"},{id:"5.8",t:"Org",n:"Information security in project management"},{id:"5.9",t:"Org",n:"Inventory of information and other associated assets"},{id:"5.10",t:"Org",n:"Acceptable use of information and other associated assets"},{id:"5.11",t:"Org",n:"Return of assets"},{id:"5.12",t:"Org",n:"Classification of information"},{id:"5.13",t:"Org",n:"Labelling of information"},{id:"5.14",t:"Org",n:"Information transfer"},{id:"5.15",t:"Org",n:"Access control"},{id:"5.16",t:"Org",n:"Identity management"},{id:"5.17",t:"Org",n:"Authentication information"},{id:"5.18",t:"Org",n:"Access rights"},{id:"5.19",t:"Org",n:"Information security in supplier relationships"},{id:"5.20",t:"Org",n:"Addressing information security within supplier agreements"},{id:"5.21",t:"Org",n:"Managing information security in the ICT supply chain"},{id:"5.22",t:"Org",n:"Monitoring, review and change management of supplier services"},{id:"5.23",t:"Org",n:"Information security for use of cloud services"},{id:"5.24",t:"Org",n:"Information security incident management planning and preparation"},{id:"5.25",t:"Org",n:"Assessment and decision on information security events"},{id:"5.26",t:"Org",n:"Response to information security incidents"},{id:"5.27",t:"Org",n:"Learning from information security incidents"},{id:"5.28",t:"Org",n:"Collection of evidence"},{id:"5.29",t:"Org",n:"Information security during disruption"},{id:"5.30",t:"Org",n:"ICT readiness for business continuity"},{id:"5.31",t:"Org",n:"Legal, statutory, regulatory and contractual requirements"},{id:"5.32",t:"Org",n:"Intellectual property rights"},{id:"5.33",t:"Org",n:"Protection of records"},{id:"5.34",t:"Org",n:"Privacy and protection of PII"},{id:"5.35",t:"Org",n:"Independent review of information security"},{id:"5.36",t:"Org",n:"Compliance with policies, rules and standards"},{id:"5.37",t:"Org",n:"Documented operating procedures"},
// People
{id:"6.1",t:"People",n:"Screening"},{id:"6.2",t:"People",n:"Terms and conditions of employment"},{id:"6.3",t:"People",n:"Information security awareness, education and training"},{id:"6.4",t:"People",n:"Disciplinary process"},{id:"6.5",t:"People",n:"Responsibilities after termination or change of employment"},{id:"6.6",t:"People",n:"Confidentiality or non-disclosure agreements"},{id:"6.7",t:"People",n:"Remote working"},{id:"6.8",t:"People",n:"Information security event reporting"},
// Physical
{id:"7.1",t:"Phys",n:"Physical security perimeters"},{id:"7.2",t:"Phys",n:"Physical entry"},{id:"7.3",t:"Phys",n:"Securing offices, rooms and facilities"},{id:"7.4",t:"Phys",n:"Physical security monitoring"},{id:"7.5",t:"Phys",n:"Protecting against physical and environmental threats"},{id:"7.6",t:"Phys",n:"Working in secure areas"},{id:"7.7",t:"Phys",n:"Clear desk and clear screen"},{id:"7.8",t:"Phys",n:"Equipment siting and protection"},{id:"7.9",t:"Phys",n:"Security of assets off-premises"},{id:"7.10",t:"Phys",n:"Storage media"},{id:"7.11",t:"Phys",n:"Supporting utilities"},{id:"7.12",t:"Phys",n:"Cabling security"},{id:"7.13",t:"Phys",n:"Information disposal"},{id:"7.14",t:"Phys",n:"Secure disposal or re-use of equipment"},
// Technological
{id:"8.1",t:"Tech",n:"User end point devices"},{id:"8.2",t:"Tech",n:"Privileged access rights"},{id:"8.3",t:"Tech",n:"Information access restriction"},{id:"8.4",t:"Tech",n:"Access to source code"},{id:"8.5",t:"Tech",n:"Secure authentication"},{id:"8.6",t:"Tech",n:"Capacity management"},{id:"8.7",t:"Tech",n:"Protection against malware"},{id:"8.8",t:"Tech",n:"Management of technical vulnerabilities"},{id:"8.9",t:"Tech",n:"Configuration management"},{id:"8.10",t:"Tech",n:"Information deletion"},{id:"8.11",t:"Tech",n:"Data masking"},{id:"8.12",t:"Tech",n:"Prevention of data leakage"},{id:"8.13",t:"Tech",n:"Information backup"},{id:"8.14",t:"Tech",n:"Redundancy of information processing facilities"},{id:"8.15",t:"Tech",n:"Logging"},{id:"8.16",t:"Tech",n:"Monitoring activities"},{id:"8.17",t:"Tech",n:"Clock synchronization"},{id:"8.18",t:"Tech",n:"Use of privileged utility programs"},{id:"8.19",t:"Tech",n:"Installation of software"},{id:"8.20",t:"Tech",n:"Networks security"},{id:"8.21",t:"Tech",n:"Security of network services"},{id:"8.22",t:"Tech",n:"Segregation of networks"},{id:"8.23",t:"Tech",n:"Web filtering"},{id:"8.24",t:"Tech",n:"Use of cryptography"},{id:"8.25",t:"Tech",n:"Secure development life cycle"},{id:"8.26",t:"Tech",n:"Application security requirements"},{id:"8.27",t:"Tech",n:"Secure system architecture and engineering principles"},{id:"8.28",t:"Tech",n:"Secure coding"},{id:"8.29",t:"Tech",n:"Security testing in development and acceptance"},{id:"8.30",t:"Tech",n:"Outsourced development"},{id:"8.31",t:"Tech",n:"Separation of development, test and production environments"},{id:"8.32",t:"Tech",n:"Change management"},{id:"8.33",t:"Tech",n:"Test information"},{id:"8.34",t:"Tech",n:"Protection of information systems during audit testing"}
];
var activeTheme="all";
function render(){
  var q=document.getElementById("search").value.toLowerCase();
  var list=document.getElementById("list"); list.innerHTML="";
  var filtered=C.filter(function(c){
    if(activeTheme!=="all" && c.t!==activeTheme) return false;
    if(q && (c.id+c.n).toLowerCase().indexOf(q)===-1) return false;
    return true;
  });
  if(!filtered.length){ list.innerHTML="<p style='color:var(--muted)'>No controls match your search.</p>"; return; }
  filtered.forEach(function(c){
    var d=document.createElement("div"); d.className="ctrl";
    d.innerHTML="<span class='ctrl-id'>A."+c.id+"</span> <span class='ctrl-theme'>"+c.t+"</span><br><strong style='color:#fff'>"+c.n+"</strong>";
    list.appendChild(d);
  });
}
document.getElementById("search").oninput=render;
document.querySelectorAll(".filters button").forEach(function(b){
  b.onclick=function(){
    document.querySelector(".filters button.active").classList.remove("active");
    b.classList.add("active");
    activeTheme=b.dataset.theme;
    render();
  };
});
render();
</script>
{% endblock %}"""
open("backend/templates/tools/iso27001_control_finder.html", "w", encoding="utf-8").write(control_finder)
print("[CREATED] tools/iso27001_control_finder.html")

# ================= 3. UPDATE INDEX & ROUTES =================
ti = "backend/templates/tools/index.html"
c = open(ti, encoding="utf-8").read()
c = c.replace('<div class="card"><h3>Security Policy Generator</h3><p>Generate professional draft documents.</p><span style="color:var(--muted)">Coming soon</span></div>', '<div class="card"><h3>Security Policy Generator</h3><p>Draft InfoSec, Password, and AUP policies instantly.</p><a href="/tools/security-policy-generator">Use Tool &rarr;</a></div>')
c = c.replace('<div class="card"><h3>ISO 27001 Control Finder</h3><p>Search the 93 controls of Annex A.</p><span style="color:var(--muted)">Coming soon</span></div>', '<div class="card"><h3>ISO 27001 Control Finder</h3><p>Search and filter the 93 Annex A (2022) controls.</p><a href="/tools/iso27001-control-finder">Use Tool &rarr;</a></div>')
open(ti, "w", encoding="utf-8").write(c)
print("[UPDATED] tools index")

sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if "security-policy-generator" not in r:
    anchor = '@router.get("/careers", response_class=HTMLResponse)'
    routes = '''@router.get("/tools/security-policy-generator", response_class=HTMLResponse)
async def security_policy_generator(request: Request):
    return templates.TemplateResponse("tools/security_policy_generator.html", {"request": request})

@router.get("/tools/iso27001-control-finder", response_class=HTMLResponse)
async def iso27001_control_finder(request: Request):
    return templates.TemplateResponse("tools/iso27001_control_finder.html", {"request": request})

'''
    r = r.replace(anchor, routes + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[UPDATED] site_routes.py")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Phase 7a: Security Policy Generator + ISO 27001 Control Finder"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
