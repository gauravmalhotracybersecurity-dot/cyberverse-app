import os, re, subprocess

# 0. Safety check: do the tool templates exist?
t1 = os.path.exists("backend/templates/tools/security_policy_generator.html")
t2 = os.path.exists("backend/templates/tools/iso27001_control_finder.html")
print("[CHECK] policy generator template:", "OK" if t1 else "MISSING")
print("[CHECK] control finder template:", "OK" if t2 else "MISSING")
if not (t1 and t2):
    print("[!] Templates missing - re-run the Phase 7a script first, then this one.")

# 1. Append new cards to tools index
ti = "backend/templates/tools/index.html"
c = open(ti, encoding="utf-8").read()
if "Security Policy Generator" not in c:
    anchor = '<div class="card"><h3>Career Roadmap Generator</h3><p>Get a 6-month SOC / GRC roadmap.</p><a href="/app.html">Try in CyberVerse AI &rarr;</a></div>'
    new_cards = anchor + '''
  <div class="card"><h3>Security Policy Generator</h3><p>Draft InfoSec, Password, AUP and IR policies instantly.</p><a href="/tools/security-policy-generator">Use Tool &rarr;</a></div>
  <div class="card"><h3>ISO 27001 Control Finder</h3><p>Search and filter the 93 Annex A (2022) controls.</p><a href="/tools/iso27001-control-finder">Use Tool &rarr;</a></div>
  <div class="card"><h3>Incident Severity Calculator</h3><p>Classify incidents and pick the right response track.</p><span style="color:var(--muted)">Coming soon</span></div>
  <div class="card"><h3>Vendor Risk Assessment</h3><p>Questionnaire-based third-party risk rating.</p><span style="color:var(--muted)">Coming soon</span></div>'''
    if anchor in c:
        c = c.replace(anchor, new_cards)
        print("[FIXED] cards appended after Career Roadmap card")
    else:
        m = re.search(r'</div>\s*{% endblock %}', c)
        if m:
            c = c[:m.start()] + new_cards + "\n" + c[m.start():]
            print("[FIXED] cards inserted via fallback")
    open(ti, "w", encoding="utf-8").write(c)

# 2. Ensure routes exist
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if "security-policy-generator" not in r:
    anchor = '@router.get("/b2b", response_class=HTMLResponse)'
    if anchor not in r:
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
    print("[FIXED] routes added")
else:
    print("[OK] routes already present")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: add Policy Generator + Control Finder cards to tools index"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
