import re, glob, subprocess

NEW_JS = r'''const ROADMAPS = {
 soc: { label: "SOC Analyst", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking & Linux basics", tag: "Security+ SY0-701.1-1.3", items: ["TCP/IP, OSI model", "Linux permissions", "Quiz me on ports"] },
   { t: "Security fundamentals", tag: "Security+ SY0-701.1.4-2.2", items: ["CIA triad, AAA, zero trust", "Malware types, phishing", "Solve a CTF Bite"] },
   { t: "Threat landscape & MITRE ATT&CK", tag: "ATT&CK", items: ["Navigate the ATT&CK matrix", "Map 3 real breaches to TTPs", "Quiz on tactics vs techniques"] },
   { t: "Logging & SIEM basics", tag: "Splunk Fundamentals", items: ["Install Splunk free tier", "Ingest Sysmon logs", "Write your first SPL query"] } ] },
  { name: "Phase 2 - Detection & Response", weeks: [
   { t: "Alert triage drills", tag: "Practice", items: ["True vs false positive drills", "Phishing triage playbook", "Write an escalation note"] },
   { t: "Use-case building", tag: "Splunk Core", items: ["Correlation search basics", "Threshold tuning", "Document one use case end-to-end"] },
   { t: "Threat intel workflow", tag: "CTI", items: ["IOC vs TTP thinking", "Enrich an alert with intel", "Write an intel summary"] },
   { t: "Incident response basics", tag: "IR", items: ["PICERL lifecycle", "Contain a mock ransomware case", "Evidence handling quiz"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Triage case studies", tag: "Portfolio", items: ["Write 2 triage case studies", "Publish on LinkedIn", "Peer review exchange"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Keyword-map to SOC JDs", "Rewrite bullets with metrics", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain detections out loud", "Apply feedback loop"] },
   { t: "Lab showcase", tag: "Lab Log", items: ["Polish home-lab writeups", "Link labs in resume", "Demo one lab in interview"] } ] } ] },
 grc: { label: "GRC Consultant", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "GRC & frameworks map", tag: "ISO 27001", items: ["Governance, Risk, Compliance pillars", "ISO vs SOC 2 vs NIST CSF", "Quiz on clauses 4-10"] },
   { t: "Risk fundamentals", tag: "ISO 27001 6.1", items: ["5x5 likelihood-impact method", "Risk appetite vs tolerance", "Score 5 sample risks"] },
   { t: "Controls & Annex A", tag: "Annex A", items: ["4 themes overview (93 controls)", "Map 10 controls to risks", "Control Finder drill"] },
   { t: "Policies & documentation", tag: "Practice", items: ["Draft an InfoSec policy", "Version control basics", "Policy review cycle"] } ] },
  { name: "Phase 2 - Practice", weeks: [
   { t: "Gap assessment run", tag: "Practice", items: ["Run gap tool on a fictional company", "Prioritize findings", "Write remediation plan"] },
   { t: "Risk register mastery", tag: "Register", items: ["Build a 15-row register", "Assign owners & target dates", "Justify treatments"] },
   { t: "Vendor risk management", tag: "VRM", items: ["Design a vendor questionnaire", "Score 3 vendors", "Contract clauses quiz"] },
   { t: "Compliance monitoring", tag: "Audit", items: ["Evidence collection routines", "Define KPIs & metrics", "Prep a management review"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "SoA & audit prep", tag: "SoA", items: ["Build a Statement of Applicability", "Justify excluded controls", "Internal audit checklist"] },
   { t: "GRC case studies", tag: "Portfolio", items: ["Write 2 GRC case studies", "Publish on LinkedIn", "Peer review exchange"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["GRC keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain your risk method out loud", "Apply feedback loop"] } ] } ] },
 seceng: { label: "Security Engineer", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking deep-dive", tag: "Security+", items: ["Subnetting, routing, TLS handshake", "Packet capture lab", "Ports & protocols quiz"] },
   { t: "Linux & scripting", tag: "Linux", items: ["Hardening basics", "Automate a task in Bash", "Cron + logging lab"] },
   { t: "Identity & access", tag: "IAM", items: ["MFA/SSO/OAuth flows", "Break-fix AD lab", "Design least privilege"] },
   { t: "Cloud fundamentals", tag: "Cloud", items: ["Core AWS/Azure services", "IAM policies lab", "Shared responsibility model"] } ] },
  { name: "Phase 2 - Engineering", weeks: [
   { t: "Secure architecture", tag: "Design", items: ["Segmentation design", "WAF/proxy placement", "Threat-model a web app"] },
   { t: "Hardening & baselines", tag: "CIS", items: ["CIS benchmarks overview", "Harden a VM lab", "Config drift check"] },
   { t: "Detection engineering", tag: "SIEM", items: ["Write 3 detection rules", "Tune false positives", "Document coverage"] },
   { t: "DevSecOps basics", tag: "CI/CD", items: ["SAST/DAST/SCA gates", "Secret scanning", "Fix a vulnerable pipeline"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Engineering writeups", tag: "Lab Log", items: ["3 build/harden writeups", "Architecture diagrams", "Publish them"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Engineering keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Whiteboard TLS & OAuth", "Apply feedback loop"] },
   { t: "System design drill", tag: "Design", items: ["Design a secure SaaS edge", "Discuss tradeoffs out loud", "Peer review"] } ] } ] },
 auditor: { label: "ISO 27001 Auditor", phases: [
  { name: "Phase 1 - Standard mastery", weeks: [
   { t: "Clauses 4-7 deep-dive", tag: "ISO 27001", items: ["Context & leadership", "Planning & support", "Clause quiz"] },
   { t: "Clauses 8-10 + Annex A", tag: "ISO 27001", items: ["Operation & improvement", "Scan all 93 controls", "Mapping exercise"] },
   { t: "Audit principles", tag: "ISO 19011", items: ["Audit types & ethics", "Programme management", "Auditor competence"] },
   { t: "Documentation review", tag: "Practice", items: ["Review sample ISMS docs", "Find 10 gaps", "Write review notes"] } ] },
  { name: "Phase 2 - Auditing", weeks: [
   { t: "Audit planning", tag: "Practice", items: ["Scope & criteria", "Audit plan & checklist", "Sampling methods"] },
   { t: "Interviewing auditees", tag: "Practice", items: ["Open-question technique", "Evidence vs assertion", "Note-taking drill"] },
   { t: "Nonconformity writing", tag: "NC", items: ["Major vs minor NC", "Root-cause phrasing", "Write 5 NC statements"] },
   { t: "Stage 1 & Stage 2 mock", tag: "Audit", items: ["Run a mock Stage 1", "Run a mock Stage 2", "Write the audit report"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Lead Auditor prep", tag: "ISO LA", items: ["Exam syllabus map", "Practice questions", "Case studies"] },
   { t: "Auditor portfolio", tag: "Portfolio", items: ["Sample audit report", "Checklist pack", "Publish a summary"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Auditor keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Defend NC decisions out loud", "Apply feedback loop"] } ] } ] },
 pentest: { label: "Penetration Tester", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking & web basics", tag: "Security+", items: ["HTTP, DNS, TLS in depth", "Burp Suite setup", "Recon basics"] },
   { t: "Linux & tooling", tag: "Linux", items: ["CLI fluency drills", "nmap/nuclei basics", "Build your lab"] },
   { t: "Web vulns I", tag: "OWASP", items: ["Injection & XSS labs", "Burp Repeater drills", "7 writeups"] },
   { t: "Web vulns II", tag: "OWASP", items: ["AuthN/Z & SSRF labs", "API testing basics", "7 writeups"] } ] },
  { name: "Phase 2 - Practice", weeks: [
   { t: "Network pentest basics", tag: "eJPT", items: ["Scanning & enumeration", "Priv-esc basics", "Report writing"] },
   { t: "Active Directory labs", tag: "AD", items: ["Kerberos attacks overview", "Lateral movement lab", "Detection awareness"] },
   { t: "Reporting & communication", tag: "Report", items: ["Executive vs technical", "Risk rating with CVSS", "Remediation advice"] },
   { t: "CTF grind", tag: "CTF", items: ["4 easy HTB boxes", "Time-boxed methodology", "Build your notes system"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Specialty depth", tag: "OSCP-prep", items: ["Pick web-API or AD", "20 focused labs", "Mentor review"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Pentest keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain exploit chains out loud", "Apply feedback loop"] },
   { t: "Portfolio & ethics", tag: "Ethics", items: ["Public writeups", "Scope & rules of engagement", "Demo day"] } ] } ] }
};
function rmRole(){ try { return localStorage.getItem("cv_rm_role") || "soc"; } catch(e){ return "soc"; } }
function syncCoachRole(label){
  var sel = document.querySelector("#view-interview select");
  if (!sel) return;
  for (var i = 0; i < sel.options.length; i++) {
    if (sel.options[i].text === label) { sel.value = sel.options[i].value; break; }
  }
}
function renderRoadmap() {
  try {
    if (localStorage.getItem("cv_roadmap") && !localStorage.getItem("cv_roadmap_soc")) {
      localStorage.setItem("cv_roadmap_soc", localStorage.getItem("cv_roadmap"));
    }
  } catch(e) {}
  var role = rmRole();
  var R = ROADMAPS[role] || ROADMAPS.soc;
  var view = document.getElementById("view-roadmap");
  if (view) {
    var h1 = view.querySelector(".view-title");
    if (h1) h1.textContent = "\ud83d\uddfa\ufe0f 90-Day " + R.label + " Roadmap";
  }
  var list = document.getElementById("rm-list");
  if (!list) return;
  var chips = document.getElementById("rm-roles");
  if (!chips) {
    chips = document.createElement("div");
    chips.id = "rm-roles";
    chips.style.cssText = "display:flex;gap:.5rem;flex-wrap:wrap;margin:10px 0 18px";
    list.parentNode.insertBefore(chips, list);
  }
  chips.innerHTML = "";
  Object.keys(ROADMAPS).forEach(function(k){
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = ROADMAPS[k].label;
    b.style.cssText = "padding:6px 12px;border-radius:16px;font-size:.8rem;cursor:pointer;border:1px solid #333;background:#151515;color:#fff;" + (k === role ? "background:var(--accent);color:#001512;border-color:var(--accent);font-weight:700;" : "");
    b.onclick = function(){
      try { localStorage.setItem("cv_rm_role", k); } catch(e) {}
      syncCoachRole(ROADMAPS[k].label);
      renderRoadmap();
    };
    chips.appendChild(b);
  });
  var storeKey = "cv_roadmap_" + role;
  var done = {};
  try { done = JSON.parse(localStorage.getItem(storeKey) || "{}"); } catch(e) {}
  var total = 0, doneCount = 0;
  R.phases.forEach(function(p){ p.weeks.forEach(function(w){ total++; if (done[R.phases.indexOf(p) + "-" + p.weeks.indexOf(w)]) doneCount++; }); });
  var bar = document.getElementById("rm-bar");
  if (bar) bar.style.width = Math.round(100 * doneCount / total) + "%";
  var prog = document.getElementById("rm-progress");
  if (prog) prog.textContent = doneCount + " / " + total + " weeks completed";
  list.innerHTML = "";
  R.phases.forEach(function(ph, pi){
    var hd = document.createElement("h2");
    hd.style.cssText = "color:var(--accent);margin:18px 0 10px;font-size:1.15rem";
    hd.textContent = ph.name;
    list.appendChild(hd);
    ph.weeks.forEach(function(w, wi){
      var key = pi + "-" + wi;
      var itemsHtml = "";
      for (var i = 0; i < w.items.length; i++) { itemsHtml += "<li>" + w.items[i] + "</li>"; }
      var card = document.createElement("div");
      card.style.cssText = "background:#141414;border:1px solid #222;border-radius:12px;padding:16px;margin-bottom:12px";
      card.innerHTML = "<div style='display:flex;gap:12px;align-items:flex-start'><input type='checkbox' data-key='" + key + "' style='width:20px;height:20px;margin-top:4px;flex:none'" + (done[key] ? " checked" : "") + "><div><div style='font-weight:700;color:#fff;font-size:1.05rem'>" + w.t + " <span style='border:1px solid #f5af19;color:#f5af19;border-radius:14px;padding:2px 10px;font-size:.75rem;font-weight:600;margin-left:6px;white-space:nowrap'>" + w.tag + "</span></div><ul style='color:var(--text-muted);margin:8px 0 0;padding-left:18px;line-height:1.7'>" + itemsHtml + "</ul><button class='btn-secondary rm-go' data-goto='interview' style='margin-top:10px;padding:6px 14px'>Practice \u2192</button></div></div>";
      list.appendChild(card);
    });
  });
  var cbs = list.querySelectorAll("input[type=checkbox]");
  for (var c = 0; c < cbs.length; c++) {
    cbs[c].addEventListener("change", function(){
      var d = {};
      try { d = JSON.parse(localStorage.getItem(storeKey) || "{}"); } catch(e) {}
      d[this.dataset.key] = this.checked;
      try { localStorage.setItem(storeKey, JSON.stringify(d)); } catch(e) {}
      renderRoadmap();
    });
  }
  var gos = list.querySelectorAll(".rm-go");
  for (var g = 0; g < gos.length; g++) {
    gos[g].addEventListener("click", function(){ goToView(this.dataset.goto); });
  }
}
'''

# Self-check brace/paren balance BEFORE touching anything
ok = (NEW_JS.count("{") == NEW_JS.count("}")) and (NEW_JS.count("(") == NEW_JS.count(")")) and (NEW_JS.count("[") == NEW_JS.count("]"))
print("[SELFCHECK] braces/parens/brackets balanced:", ok)
if not ok:
    raise SystemExit("ABORT: replacement JS not balanced - nothing was changed")

for jf in ["app.js", "app2.js"]:
    for f in [x for x in glob.glob("**/" + jf, recursive=True) if not any(t in x for t in ("venv", "node_modules", ".git"))]:
        c = open(f, encoding="utf-8").read()
        end = c.find("const LABS = [")
        start = c.find("const ROADMAPS = {")
        if start == -1:
            start = c.find("const ROADMAP = [")
        if start == -1 or end == -1 or end < start:
            print("[SKIP] anchors not found in", f)
            continue
        c = c[:start] + NEW_JS + "\n\n" + c[end:]
        open(f, "w", encoding="utf-8").write(c)
        print("[FIXED] replaced broken roadmap span in", f)

# Cache-bust script tags in app.html
for f in [x for x in glob.glob("**/app.html", recursive=True) if not any(t in x for t in ("venv", "node_modules", ".git"))]:
    c = open(f, encoding="utf-8").read()
    c2 = re.sub(r'(src=["\'])app2\.js(?:\?v=[A-Za-z0-9]+)?(["\'])', r'\1app2.js?v=20260907b\2', c)
    c2 = re.sub(r'(src=["\'])app\.js(?:\?v=[A-Za-z0-9]+)?(["\'])', r'\1app.js?v=20260907b\2', c2)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        print("[CACHE-BUST] script tags versioned in", f)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix+Feature: brace-balanced role-aware roadmaps v2 + cache-bust"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED - watch Render deploy now")
