import glob, os, subprocess
skip = ("venv", "node_modules", ".git")

# 1. Add audience endpoint (read-only, admin-gated)
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
if '"/admin/audience"' not in c:
    endpoint = '''

@router.get("/admin/audience")
def admin_audience(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    if not _is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")
    out = {"subs": [], "leads": []}
    try:
        rows = db.execute(_t("SELECT email, source, created_at FROM newsletter_subs ORDER BY created_at DESC LIMIT 500")).fetchall()
        out["subs"] = [{"email": r[0], "source": r[1], "created_at": r[2]} for r in rows]
    except Exception:
        pass
    try:
        rows = db.execute(_t("SELECT email, source, created_at FROM leads ORDER BY created_at DESC LIMIT 500")).fetchall()
        out["leads"] = [{"email": r[0], "source": r[1], "created_at": r[2]} for r in rows]
    except Exception:
        pass
    return out
'''
    c += endpoint
    # Compile-check before writing
    try:
        compile(c, ar, "exec")
        open(ar, "w", encoding="utf-8").write(c)
        print("[BACKEND] Audience endpoint added (compile-verified)")
    except SyntaxError as e:
        print(f"[ABORT] Syntax error: {e}")
        raise SystemExit(1)

# 2. Add UI to admin_leads.html
tdir = None
for root, dirs, files in os.walk("."):
    if any(t in root for t in skip): continue
    if os.path.basename(root) == "templates" and "backend" in root.replace("\\", "/"):
        tdir = root; break
al = os.path.join(tdir, "admin_leads.html")
h = open(al, encoding="utf-8").read()
if "subsbox" not in h:
    h = h.replace('<div id="content"></div>',
        '<div id="content"></div>\n  <h2 style="color:#fff;margin-top:2rem">Newsletter subscribers</h2>\n  <div id="subsbox" style="color:var(--muted)">Loading...</div>\n  <h2 style="color:#fff;margin-top:1.5rem">Other leads (exit popup / starter kit)</h2>\n  <div id="leadsbox" style="color:var(--muted)">Loading...</div>')
    aud_js = '''
fetch("/api/analytics/admin/audience", {headers:{"Authorization":"Bearer "+TOKEN}})
.then(function(r){ if(!r.ok) throw new Error("auth"); return r.json(); })
.then(function(d){
  function tbl(rows, cols){
    if(!rows.length) return "<p style='color:var(--muted)'>None yet.</p>";
    var h = "<table class='tbl'><tr>" + cols.map(function(c){ return "<th>"+c+"</th>"; }).join("") + "</tr>";
    rows.forEach(function(r){ h += "<tr><td>"+esc(r.email)+"</td><td>"+esc(r.source)+"</td><td>"+esc(fmt(r.created_at))+"</td></tr>"; });
    return h + "</table>";
  }
  document.getElementById("subsbox").innerHTML = tbl(d.subs, ["Email","Source","When"]);
  document.getElementById("leadsbox").innerHTML = tbl(d.leads, ["Email","Source","When"]);
})
.catch(function(){ document.getElementById("subsbox").innerHTML = "<p style='color:var(--muted)'>Not authorized.</p>"; document.getElementById("leadsbox").innerHTML = ""; });
'''
    h = h.replace("</script>", aud_js + "</script>", 1)
    open(al, "w", encoding="utf-8").write(h)
    print("[UI] Audience section added to admin-leads")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Audience: subscriber/lead visibility in admin (compile-verified)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
