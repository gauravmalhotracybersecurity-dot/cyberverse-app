import glob, os, subprocess
skip = ("venv", "node_modules", ".git")
tdir = None
for root, dirs, files in os.walk("."):
    if any(t in root for t in skip): continue
    if os.path.basename(root) == "templates" and "backend" in root.replace("\\", "/"):
        tdir = root; break

# ---------- admin_leads.html ----------
p = os.path.join(tdir, "admin_leads.html")
c = open(p, encoding="utf-8").read()
n = 0

old_head = ' <h1 style="color:#fff">B2B Leads <span style="color:var(--muted);font-size:1rem;font-weight:400">/ admin</span></h1>\n <p style="color:var(--muted">Submissions from the "Get a Free GRC Assessment" funnel. &middot; <a href="/admin-payments" style="color:var(--accent)">View payments &amp; subscriptions &rarr;</a></p>\n'
new_head = ' <div id="admin-head" style="display:none">\n <h1 style="color:#fff">B2B Leads <span style="color:var(--muted);font-size:1rem;font-weight:400">/ admin</span></h1>\n <p style="color:var(--muted">Submissions from the "Get a Free GRC Assessment" funnel. &middot; <a href="/admin-payments" style="color:var(--accent)">View payments &amp; subscriptions &rarr;</a></p>\n </div>\n <div id="checking" style="padding:3rem;text-align:center;color:var(--muted)">Verifying access&hellip;</div>\n'
if old_head in c:
    c = c.replace(old_head, new_head, 1); n += 1

gate = ' <div id="gate" class="gate" style="display:none">\n   <h2>Not signed in</h2>\n   <p><a href="/app.html">Log in to CyberVerse AI</a>, then reload this page.</p>\n </div>\n'
if gate in c:
    c = c.replace(gate, "", 1); n += 1

old401 = 'if(r.status === 401 || r.status === 403){ document.getElementById("gate").style.display="block"; document.getElementById("app").style.display="none"; throw new Error("auth"); }'
new401 = 'if(r.status === 401 || r.status === 403){ location.replace("/app.html"); throw new Error("auth"); }'
if old401 in c:
    c = c.replace(old401, new401, 1); n += 1

oldboot = 'if(!TOKEN){\n  document.getElementById("gate").style.display = "block";\n} else {\n  load();\n}'
newboot = 'if(!TOKEN){ location.replace("/app.html"); } else { load(); }'
if oldboot in c:
    c = c.replace(oldboot, newboot, 1); n += 1

oldok = '  document.getElementById("app").style.display = "block";'
newok = oldok + '\n  var _h=document.getElementById("admin-head"); if(_h)_h.style.display="block";\n  var _c=document.getElementById("checking"); if(_c)_c.style.display="none";'
if oldok in c:
    c = c.replace(oldok, newok, 1); n += 1

open(p, "w", encoding="utf-8").write(c)
print("[admin_leads] patches applied:", n)

# ---------- admin_payments.html ----------
p = os.path.join(tdir, "admin_payments.html")
c = open(p, encoding="utf-8").read()
n = 0

old_head = ' <h1 style="color:#fff">Payments &amp; Subscriptions <span style="color:var(--muted);font-size:1rem;font-weight:400">/ admin</span></h1>\n <p class="hint"><a href="/admin-leads" style="color:var(--accent)">&larr; B2B leads</a></p>\n <div id="gate" class="gate" style="display:none"><h2>Not signed in</h2><p><a href="/app.html">Log in</a>, then reload.</p></div>\n'
new_head = ' <div id="admin-head" style="display:none">\n <h1 style="color:#fff">Payments &amp; Subscriptions <span style="color:var(--muted);font-size:1rem;font-weight:400">/ admin</span></h1>\n <p class="hint"><a href="/admin-leads" style="color:var(--accent)">&larr; B2B leads</a></p>\n </div>\n <div id="checking" style="padding:3rem;text-align:center;color:var(--muted)">Verifying access&hellip;</div>\n'
if old_head in c:
    c = c.replace(old_head, new_head, 1); n += 1

old401 = '.then(function(r){ if(r.status===401||r.status===403){ document.getElementById("gate").style.display="block"; throw new Error("auth"); } return r.json(); })'
new401 = '.then(function(r){ if(r.status===401||r.status===403){ location.replace("/app.html"); throw new Error("auth"); } return r.json(); })'
if old401 in c:
    c = c.replace(old401, new401, 1); n += 1

oldok = '  document.getElementById("app").style.display = "block";'
newok = oldok + '\n  var _h=document.getElementById("admin-head"); if(_h)_h.style.display="block";\n  var _c=document.getElementById("checking"); if(_c)_c.style.display="none";'
if oldok in c:
    c = c.replace(oldok, newok, 1); n += 1

oldprice = 'var PRICE = {pro: 499, premium: 999};'
newprice = oldprice + '\nif(!TOKEN){ location.replace("/app.html"); }'
if oldprice in c and "if(!TOKEN){ location.replace" not in c:
    c = c.replace(oldprice, newprice, 1); n += 1

open(p, "w", encoding="utf-8").write(c)
print("[admin_payments] patches applied:", n)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Security: admin pages bounce non-admins, render zero admin UI unauthenticated"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
