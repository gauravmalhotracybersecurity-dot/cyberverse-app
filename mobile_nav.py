import subprocess, re

p = "backend/templates/base.html"
c = open(p, encoding="utf-8").read()

# Show current header markup for reference
i = c.find("<nav")
if i >= 0:
    print("=== CURRENT NAV MARKUP ===")
    print(c[max(0,i-300):i+500])
    print("=========================\n")

if "nav-toggle" in c:
    print("[SKIP] mobile nav already present")
else:
    # 1. Locate the nav containing /learn
    idx = c.find("<nav")
    while idx >= 0 and "/learn" not in c[idx:idx+2000]:
        idx = c.find("<nav", idx + 4)
    if idx < 0:
        print("[ERROR] no <nav> with /learn found - paste header markup for manual fix")
        raise SystemExit(1)

    # 2. Give it an id
    if 'id="main-nav"' not in c[idx:idx+200]:
        c = c[:idx] + c[idx:].replace("<nav", '<nav id="main-nav"', 1)
        print("[TAGGED] nav id=main-nav")

    # 3. Insert hamburger button right before the nav
    btn = '<button id="nav-toggle" aria-label="Open menu" style="display:none;background:none;border:1px solid #333;color:var(--accent);font-size:1.3rem;border-radius:8px;padding:2px 12px;cursor:pointer;margin-left:auto">&#9776;</button>'
    c = c[:idx] + btn + c[idx:]
    print("[ADDED] hamburger button")

    # 4. Mobile CSS (new style block before </head>)
    css = '''
<style>
@media (max-width: 900px) {
  #nav-toggle { display:inline-block !important; }
  #main-nav { display:none; position:fixed; top:64px; left:0; right:0; max-height:calc(100vh - 64px); overflow-y:auto; background:#0a0a0a; border-bottom:1px solid #222; flex-direction:column; align-items:stretch; padding:.5rem 1.2rem 1.2rem; z-index:300; gap:0 !important; }
  #main-nav.open { display:flex; }
  #main-nav a { padding:.8rem 0 !important; border-bottom:1px solid #1a1a1a; font-size:1rem; }
  #main-nav a.nav-cta { margin-top:.8rem; text-align:center; border-bottom:none; }
}
</style>
'''
    h = c.find("</head>")
    c = c[:h] + css + c[h:]
    print("[ADDED] mobile nav CSS")

    # 5. Toggle JS before </body>
    js = '''
<script>
(function(){
  var t = document.getElementById("nav-toggle"), n = document.getElementById("main-nav");
  if (!t || !n) return;
  t.addEventListener("click", function(e){ e.stopPropagation(); n.classList.toggle("open"); });
  document.addEventListener("click", function(e){ if (!n.contains(e.target) && e.target !== t) n.classList.remove("open"); });
  n.addEventListener("click", function(e){ if (e.target.tagName === "A") n.classList.remove("open"); });
})();
</script>
'''
    b = c.rfind("</body>")
    c = c[:b] + js + c[b:]
    print("[ADDED] toggle JS")

    open(p, "w", encoding="utf-8").write(c)
    print("[SAVED] base.html")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Mobile: hamburger menu for nav links (Learn/Tools/Careers/Resources/Books)"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
