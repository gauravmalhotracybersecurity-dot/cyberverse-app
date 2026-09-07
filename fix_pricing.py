import re, subprocess

# 1. Add USD approx to plans config
p = "backend/plans.py"
c = open(p, encoding="utf-8").read()
c = c.replace('"price_inr": 499,', '"price_inr": 499, "price_usd": 6,')
c = c.replace('"price_inr": 999,', '"price_inr": 999, "price_usd": 12,')
open(p, "w", encoding="utf-8").write(c)
print("[CONFIG] price_usd added to plans.py")

# 2. Patch app.html paywall
a = "app.html"
import glob
cands = [f for f in glob.glob("**/app.html", recursive=True) if not any(x in f for x in ("venv","node_modules",".git"))]
a = cands[0]
h = open(a, encoding="utf-8").read()

# 2a. Wrap currency amounts in spans (covers Rs/INR variants too)
h, n = re.subn(r'(|Rs\.?|INR)\s*(499|999)', r'<span class="cv-price" data-inr="\2">\1\2</span>', h)
print(f"[PATCH] wrapped {n} price occurrences in spans")

# 2b. Clarification line inside paywall (bulletproof fallback)
clar = '<p style="text-align:center;margin:10px 0 0;font-size:.8rem;color:#9aa4b2">International users: prices are in Indian Rupees (&#8377;). Pro &#8776; $6/mo, Premium &#8776; $12/mo &mdash; billed in INR at checkout.</p>'
h2, m = re.subn(r'(<p class="modal-sub"[^>]*>Access activates)', clar + r'\1', h)
if m:
    h = h2
    print("[PATCH] clarification line inserted in paywall")
else:
    print("[WARN] paywall 'Access activates' line not found - clarification skipped")

# 2c. Locale-aware currency switcher
js = """
<script id="cv-currency">
(function(){
  function isIndia(){
    try{
      var tz=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");
      var lang=(navigator.language||"");
      return /kolkata|calcutta|india/i.test(tz)||/-IN$/i.test(lang);
    }catch(e){return false;}
  }
  var USD={"499":6,"999":12};
  function apply(){
    document.querySelectorAll(".cv-price").forEach(function(sp){
      var inr=sp.getAttribute("data-inr"); var usd=USD[inr]; if(!usd) return;
      var small="font-size:.72em;color:#9aa4b2;font-weight:600;margin-left:.4rem";
      if(isIndia()){ sp.innerHTML="\\u20b9"+inr+"<small style='"+small+"'>\\u2248 $"+usd+"/mo</small>"; }
      else { sp.innerHTML="$"+usd+"<small style='"+small+"'>/mo \\u00b7 billed as \\u20b9"+inr+" INR</small>"; }
    });
  }
  fetch("/api/analytics/plans").then(function(r){return r.json();}).then(function(pl){
    Object.keys(pl).forEach(function(k){ if(pl[k].price_usd) USD[String(pl[k].price_inr)]=pl[k].price_usd; });
    apply();
  }).catch(function(){});
  var runs=0; var t=setInterval(function(){ apply(); if(++runs>12) clearInterval(t); },1000);
  if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",apply);}else{apply();}
})();
</script>
"""
idx = h.rfind("</body>")
if "cv-currency" not in h and idx > -1:
    h = h[:idx] + js + h[idx:]
    print("[PATCH] currency switcher injected")

open(a, "w", encoding="utf-8").write(h)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Pricing: dual-currency display + INR clarification for international users"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
