import glob, os, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
n = 0

# 1. Audience endpoint (admin-gated): newsletter subs + general leads
if '"/admin/audience"' not in c:
    c += '''

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
    n += 1
    print("[BACKEND] /admin/audience endpoint added")

# 2. Notify owner on NEW newsletter subscriber
old_sub = '    db.execute(_t("INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})\n    db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})\n    db.commit()'
new_sub = '''    cur = db.execute(_t("INSERT OR IGNORE INTO newsletter_subs (email, source, created_at, unsubscribed) VALUES (:e,:s,:c,0)"), {"e": email, "s": source, "c": _dt.utcnow().isoformat()})
    db.execute(_t("UPDATE newsletter_subs SET unsubscribed=0 WHERE email=:e"), {"e": email})
    db.commit()
    try:
        if getattr(cur, "rowcount", 1) == 1:
            _nl_send({"from": NL_FROM, "to": [_os.environ.get("ADMIN_NOTIFY_EMAIL") or "gauravmalhotra.cybersecurity@gmail.com"],
                      "subject": "New newsletter subscriber: " + email,
                      "html": "<p>New subscriber: <b>" + email + "</b><br>Source: " + source + "</p><p><a href='https://grcwithgaurav.com/admin-leads'>Open admin</a></p>"})
    except Exception:
        pass'''
if old_sub in c:
    c = c.replace(old_sub, new_sub, 1); n += 1
    print("[BACKEND] subscriber notification added")

# 3. Notify owner on NEW B2B lead (anchor: the b2b INSERT + its commit)
import re as _re
m = _re.search(r'(INSERT INTO b2b_leads[\s\S]{0,400}?db\.commit\(\))', c)
if m and "_nl_send" in c and "New B2B lead" not in c:
    notify = m.group(1) + '''
    try:
        _nl_send({"from": NL_FROM, "to": [_os.environ.get("ADMIN_NOTIFY_EMAIL") or "gauravmalhotra.cybersecurity@gmail.com"],
                  "subject": "New B2B lead: " + str((payload or {}).get("company", "")),
                  "html": "<p>New B2B assessment lead:</p><ul><li>Name: " + str((payload or {}).get("name", "")) + "</li><li>Email: " + str((payload or {}).get("email", "")) + "</li><li>Company: " + str((payload or {}).get("company", "")) + "</li><li>Size: " + str((payload or {}).get("size", "")) + "</li><li>Timeline: " + str((payload or {}).get("timeline", "")) + "</li></ul><p>Requirement: " + str((payload or {}).get("requirement", "")) + "</p><p><a href='https://grcwithgaurav.com/admin-leads'>Open admin</a></p>"})
    except Exception:
        pass'''
    c = c.replace(m.group(1), notify, 1); n += 1
    print("[BACKEND] B2B lead notification added")

open(ar, "w", encoding="utf-8").write(c)

# 4. Audience UI in admin_leads.html
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
    n += 1
    print("[UI] audience section added to admin-leads")

print("total patches:", n)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Audience: subscriber/lead visibility in admin + owner notification emails"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
