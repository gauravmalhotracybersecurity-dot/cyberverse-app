import subprocess

p = "backend/templates/base.html"
c = open(p, encoding="utf-8").read()

# Remove all previous mobile nav CSS/JS attempts
import re
c = re.sub(r'<style>\s*/\*mobile-nav[^*]*\*/.*?</style>', '', c, flags=re.DOTALL)
c = re.sub(r'<style>\s*@media \(max-width: 900px\).*?#nav-toggle.*?</style>', '', c, flags=re.DOTALL)
c = re.sub(r'<script>\s*\(function\(\)\{\s*var t = document\.getElementById\("nav-toggle"\).*?</script>', '', c, flags=re.DOTALL)

# Correct CSS: hide .nav-links on mobile, show as dropdown when .open
css = '''
<style>
/*mobile-nav-v3*/
@media (max-width: 900px) {
  .nav { position:relative; }
  .nav-links { display:none; position:fixed; top:64px; left:0; right:0; max-height:calc(100vh - 64px); overflow-y:auto; background:#0a0a0a; border-bottom:1px solid #222; flex-direction:column; padding:.5rem 1.2rem 1.2rem; z-index:300; gap:0 !important; }
  .nav.open .nav-links { display:flex; }
  .nav-links a { padding:.8rem 0 !important; border-bottom:1px solid #1a1a1a; font-size:1rem; }
  .nav-links a.nav-cta { margin-top:.8rem; text-align:center; border-bottom:none; }
  #nav-toggle { display:inline-block !important; }
}
@media (min-width: 901px) {
  #nav-toggle { display:none !important; }
}
</style>
'''

# Insert before </head>
hh = c.find("</head>")
c = c[:hh] + css + c[hh:]

# Correct JS: toggle .open on the nav element, not a separate id
js = '''
<script>
(function(){
  var t = document.getElementById("nav-toggle");
  var n = document.querySelector("nav.nav");
  if (!t || !n) return;
  t.addEventListener("click", function(e){ e.preventDefault(); e.stopPropagation(); n.classList.toggle("open"); });
  document.addEventListener("click", function(e){ if (!n.contains(e.target) && !t.contains(e.target)) n.classList.remove("open"); });
  n.addEventListener("click", function(e){ if (e.target.tagName === "A") n.classList.remove("open"); });
})();
</script>
'''

bb = c.rfind("</body>")
c = c[:bb] + js + c[bb:]

open(p, "w", encoding="utf-8").write(c)
print("[UPDATED] base.html with v3 mobile nav (targets .nav-links correctly)")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Mobile nav v3: target .nav-links div + toggle on .nav element"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
