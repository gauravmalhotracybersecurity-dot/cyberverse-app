import glob, os, subprocess
skip = ("venv", "node_modules", ".git")

# 1. Endpoint: payments + abandoned orders (dialect-agnostic, no rowid)
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
if '"/admin/payments"' not in c:
    c += '''

@router.get("/admin/payments")
def admin_payments(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    out = {"subs": [], "abandoned": []}
    try:
        rows = db.execute(_t("SELECT s.user_id, s.plan, s.status, s.provider_payment_id, s.created_at, u.email FROM subscriptions s JOIN users u ON u.id = s.user_id ORDER BY s.created_at DESC LIMIT 300")).fetchall()
        out["subs"] = [{"user_id": r[0], "plan": r[1], "status": r[2], "payment_id": r[3], "created_at": r[4], "email": r[5]} for r in rows]
    except Exception:
        pass
    try:
        rows = db.execute(_t("SELECT o.order_id, o.user_id, o.plan, o.created_at, u.email FROM billing_orders o JOIN users u ON u.id = o.user_id WHERE NOT EXISTS (SELECT 1 FROM subscriptions s WHERE s.user_id = o.user_id AND s.plan = o.plan) ORDER BY o.created_at DESC LIMIT 300")).fetchall()
        out["abandoned"] = [{"order_id": r[0], "user_id": r[1], "plan": r[2], "created_at": r[3], "email": r[4]} for r in rows]
    except Exception:
        pass
    return out
'''
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] /admin/payments endpoint added")

# 2. Template
tpl = r"""{% extends "base.html" %}
{% block title %}Payments | Admin{% endblock %}
{% block head %}
<style>
 .wrap{max-width:1180px;margin:0 auto;padding:2rem}
 .gate{padding:3rem;text-align:center;color:var(--muted)} .gate a{color:var(--accent)}
 .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem}
 .stat{background:#151515;border:1px solid #222;border-radius:10px;padding:1rem}
 .stat b{font-size:1.7rem;color:#fff;display:block} .stat span{color:var(--muted);font-size:.85rem}
 @media(max-width:720px){.stats{grid-template-columns:1fr 1fr}}
 .tbl{width:100%;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;margin-bottom:2rem}
 .tbl th,.tbl td{padding:.6rem .7rem;border-bottom:1px solid #222;text-align:left;font-size:.85rem}
 .tbl th{background:#151515;color:var(--muted);font-size:.78rem;text-transform:uppercase;letter-spacing:.5px}
 .pill{padding:.15rem .6rem;border-radius:12px;font-size:.72rem;font-weight:700}
 .p-pro{background:#22c55e;color:#000} .p-premium{background:#f59e0b;color:#000} .p-ab{background:#7f1d1d;color:#fca5a5}
 .btn-sm{padding:.3rem .7rem;border-radius:6px;border:1px solid #333;background:#151515;color:#fff;cursor:pointer;font-size:.8rem}
 h2{color:#fff;margin:1.5rem 0 .8rem}
 .hint{color:var(--muted);font-size:.85rem;margin-bottom:1rem}
</style>
{% endblock %}
{% block content %}
<div class="wrap">
 <h1 style="color:#fff">Payments &amp; Subscriptions <span style="color:var(--muted);font-size:1rem;font-weight:400">/ admin</span></h1>
 <p class="hint"><a href="/admin-leads" style="color:var(--accent)">&larr; B2B leads</a></p>
 <div id="gate" class="gate" style="display:none"><h2>Not signed in</h2><p><a href="/app.html">Log in</a>, then reload.</p></div>
 <div id="app" style="display:none">
  <div class="stats" id="stats"></div>
  <h2>Active subscriptions</h2>
  <div id="subs"></div>
  <h2>Abandoned checkouts <span style="color:var(--muted);font-size:.9rem;font-weight:400">(ordered, never paid - DM them!)</span></h2>
  <p class="hint">A personal message within 24h ("saw you tried Pro - want a hand?") recovers 10-20% of these.</p>
  <div id="aband"></div>
  <button class="btn-sm" id="btn-csv">Export all (CSV)</button>
 </div>
</div>
<script>
var TOKEN = localStorage.getItem("cv_token");
var DATA = null;
var PRICE = {pro: 499, premium: 999};
function esc(s){ var d=document.createElement("div"); d.textContent=(s==null?"":s); return d.innerHTML; }
function fmt(d){ try{ return new Date(d).toLocaleString(); }catch(e){ return d||""; } }
fetch("/api/analytics/admin/payments", {headers:{"Authorization":"Bearer "+TOKEN}})
.then(function(r){ if(r.status===401||r.status===403){ document.getElementById("gate").style.display="block"; throw new Error("auth"); } return r.json(); })
.then(function(d){
  DATA = d;
  var rev = 0, pro = 0, pre = 0;
  d.subs.forEach(function(s){ if(s.status==="active"){ rev += PRICE[s.plan]||0; if(s.plan==="premium") pre++; else pro++; } });
  document.getElementById("stats").innerHTML =
    "<div class='stat'><b>&#8377;"+rev+"</b><span>Lifetime revenue</span></div>" +
    "<div class='stat'><b>"+d.subs.length+"</b><span>Subscriptions</span></div>" +
    "<div class='stat'><b>"+pro+"/"+pre+"</b><span>Pro / Premium</span></div>" +
    "<div class='stat'><b>"+d.abandoned.length+"</b><span>Abandoned carts</span></div>";
  var h = "<table class='tbl'><tr><th>When</th><th>Email</th><th>Plan</th><th>Status</th><th>Payment ID</th></tr>";
  d.subs.forEach(function(s){ h += "<tr><td>"+esc(fmt(s.created_at))+"</td><td>"+esc(s.email)+"</td><td><span class='pill p-"+s.plan+"'>"+s.plan+"</span></td><td>"+esc(s.status)+"</td><td>"+esc(s.payment_id)+"</td></tr>"; });
  h += "</table>";
  document.getElementById("subs").innerHTML = d.subs.length ? h : "<p class='hint'>No subscriptions yet.</p>";
  var a = "<table class='tbl'><tr><th>When</th><th>Email</th><th>Plan</th><th>Order ID</th><th></th></tr>";
  d.abandoned.forEach(function(o){ a += "<tr><td>"+esc(fmt(o.created_at))+"</td><td><a href='mailto:"+esc(o.email)+"?subject=Quick%20help%20with%20your%20CyberVerse%20upgrade' style='color:var(--accent)'>"+esc(o.email)+"</a></td><td><span class='pill p-ab'>"+o.plan+"</span></td><td>"+esc(o.order_id)+"</td><td><a class='btn-sm' href='mailto:"+esc(o.email)+"?subject=Quick%20help%20with%20your%20CyberVerse%20upgrade'>Email</a></td></tr>"; });
  a += "</table>";
  document.getElementById("aband").innerHTML = d.abandoned.length ? a : "<p class='hint'>No abandoned checkouts. Clean funnel!</p>";
  document.getElementById("app").style.display = "block";
})
.catch(function(e){ if(e.message!=="auth") console.log("payments admin error:", e); });
document.getElementById("btn-csv").onclick = function(){
  if(!DATA) return;
  var rows = [["section","when","email","plan","status","id"]];
  DATA.subs.forEach(function(s){ rows.push(["sub", s.created_at, s.email, s.plan, s.status, s.payment_id]); });
  DATA.abandoned.forEach(function(o){ rows.push(["abandoned", o.created_at, o.email, o.plan, "", o.order_id]); });
  var csv = rows.map(function(r){ return r.map(function(v){ v=String(v==null?"":v).replace(/"/g,'""'); return '"'+v+'"'; }).join(","); }).join("\n");
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
  a.download = "payments-"+new Date().toISOString().slice(0,10)+".csv";
  a.click();
};
</script>
{% endblock %}"""

tdir = None
for root, dirs, files in os.walk("."):
    if any(t in root for t in skip): continue
    if os.path.basename(root) == "templates" and "backend" in root.replace("\\", "/"):
        tdir = root; break
open(os.path.join(tdir, "admin_payments.html"), "w", encoding="utf-8").write(tpl)
print("[TEMPLATE] admin_payments.html created")

# 3. Route
sr = [x for x in glob.glob("**/site_routes.py", recursive=True) if not any(t in x for t in skip)][0]
r = open(sr, encoding="utf-8").read()
if '"/admin-payments"' not in r:
    anchor = '@router.get("/admin-leads", response_class=HTMLResponse)'
    block = '''@router.get("/admin-payments", response_class=HTMLResponse)
async def admin_payments_page(request: Request):
    return templates.TemplateResponse("admin_payments.html", {"request": request})

'''
    r = r.replace(anchor, block + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[ROUTE] /admin-payments added")

# 4. Cross-link from admin-leads
al = os.path.join(tdir, "admin_leads.html")
lc = open(al, encoding="utf-8").read()
if "/admin-payments" not in lc:
    lc = lc.replace('<p style="color:var(--muted">Submissions from the "Get a Free GRC Assessment" funnel.</p>',
                    '<p style="color:var(--muted">Submissions from the "Get a Free GRC Assessment" funnel. &middot; <a href="/admin-payments" style="color:var(--accent)">View payments &amp; subscriptions &rarr;</a></p>')
    open(al, "w", encoding="utf-8").write(lc)
    print("[LINK] admin-leads now links to payments")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Admin: payments & subscriptions view with abandoned-cart recovery list"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
