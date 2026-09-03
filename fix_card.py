import re, subprocess

# 1. Fix the tools index card (regex = immune to text variations)
ti = "backend/templates/tools/index.html"
c = open(ti, encoding="utf-8").read()
new_card = '<div class="card"><h3>Risk Register Generator</h3><p>Full 12-field register with owners, dates, status + CSV/PDF export.</p><a href="/tools/risk-register-generator">Use Tool &rarr;</a></div>'
c2, n = re.subn(r'<div class="card"><h3>Risk Register Generator</h3>.*?</div>', new_card, c, count=1, flags=re.S)
if n:
    open(ti, "w", encoding="utf-8").write(c2)
    print("[FIXED] Risk Register card now links to the live tool")
else:
    print("[WARN] card pattern not found")

# 2. Safety check: route exists?
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
if "risk-register-generator" not in r:
    anchor = '@router.get("/learn", response_class=HTMLResponse)'
    route = '''@router.get("/tools/risk-register-generator", response_class=HTMLResponse)
async def risk_register_generator(request: Request):
    return templates.TemplateResponse("tools/risk_register_generator.html", {"request": request})

'''
    r = r.replace(anchor, route + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[FIXED] route added")
else:
    print("[OK] route already present")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: Risk Register card link on tools index"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
