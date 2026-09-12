import subprocess, re, urllib.request

# === 1. LIVE DIAGNOSIS ===
print("=== LIVE SITE CHECK ===")
try:
    req = urllib.request.Request("https://grcwithgaurav.com/", headers={"User-Agent": "Mozilla/5.0"})
    h = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    print("  nav-toggle button live: ", 'id="nav-toggle"' in h)
    print("  main-nav id live:       ", 'id="main-nav"' in h)
    print("  toggle JS live:         ", 'classList.toggle("open")' in h)
    print("  mobile CSS live:        ", "@media (max-width: 900px)" in h)
    i = h.find("<header")
    j = h.find("</header>")
    if i >= 0 and j >= 0:
        print("\n=== LIVE HEADER MARKUP ===")
        print(h[i:j+9][:1200])
except Exception as e:
    print("  fetch error:", e)

# === 2. LOCAL REPAIR (v2 - defensive) ===
p = "backend/templates/base.html"
c = open(p, encoding="utf-8").read()

# 2a. Replace old toggle JS with defensive version
new_js = '''<script>
(function(){
  var t = document.getElementById("nav-toggle");
  var n = document.getElementById("main-nav") || document.querySelector("header nav") || document.querySelector("nav");
  if (!t || !n) return;
  if (!n.id) n.id = "main-nav";
  t.addEventListener("click", function(e){ e.preventDefault(); e.stopPropagation(); n.classList.toggle("open"); });
  document.addEventListener("click", function(e){ if (!n.contains(e.target) && !t.contains(e.target)) n.classList.remove("open"); });
  n.addEventListener("click", function(e){ if (e.target.tagName === "A") n.classList.remove("open"); });
})();
</script>'''
c2 = re.sub(r'<script>\s*\(function\(\)\{\s*var t = document\.getElementById\("nav-toggle"\).*?</script>', new_js, c, flags=re.DOTALL)
if c2 != c:
    print("\n[REPLACED] toggle JS with defensive v2")
    c = c2
elif 'id="nav-toggle"' in c and "header nav" not in c:
    print("\n[WARN] old JS not matched - will append v2")
    b = c.rfind("</body>")
    c = c[:b] + new_js + "\n" + c[b:]

# 2b. Robust CSS v2 (works via id OR header nav fallback, fixes button position)
if "/*mobile-nav-v2*/" not in c:
    css = '''
<style>
/*mobile-nav-v2*/
@media (max-width: 900px) {
  header { display:flex !important; align-items:center; justify-content:space-between; gap:1rem; }
  #nav-toggle { display:inline-block !important; order:99; margin-left:auto; }
  #main-nav, header nav { display:none; }
  #main-nav.open, header nav.open { display:flex !important; position:fixed; top:64px; left:0; right:0; max-height:calc(100vh - 64px); overflow-y:auto; background:#0a0a0a; border-bottom:1px solid #222; flex-direction:column; padding:.5rem 1.2rem 1.2rem; z-index:300; }
  #main-nav a, header nav.open a { padding:.8rem 0 !important; border-bottom:1px solid #1a1a1a; font-size:1rem; }
}
</style>
'''
    hh = c.find("</head>")
    c = c[:hh] + css + c[hh:]
    print("[ADDED] mobile CSS v2 (fallback selectors + right-aligned button)")

# 2c. Ensure button exists (fallback insert after <header> open tag)
if 'id="nav-toggle"' not in c:
    hi = c.find("<header")
    if hi >= 0:
        gt = c.find(">", hi)
        btn = '<button id="nav-toggle" aria-label="Open menu" style="display:none;background:none;border:1px solid #333;color:var(--accent);font-size:1.3rem;border-radius:8px;padding:2px 12px;cursor:pointer">&#9776;</button>'
        c = c[:gt+1] + btn + c[gt+1:]
        print("[ADDED] hamburger button (after header open tag)")
    else:
        print("[ERROR] no <header> found")

open(p, "w", encoding="utf-8").write(c)
print("[SAVED] base.html")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Mobile nav v2: defensive toggle JS + fallback CSS selectors"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
