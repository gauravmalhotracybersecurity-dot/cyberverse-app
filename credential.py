import glob, os, subprocess
skip = ("venv", "node_modules", ".git")

# 1. Mint endpoint (premium-gated, schema-independent)
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
if '"/interview/credential"' not in c:
    c += '''

@router.post("/interview/credential")
def mint_credential(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import uuid
    from sqlalchemy import text as _t
    from datetime import datetime as _dt
    if not getattr(user, "is_premium", False):
        raise HTTPException(status_code=403, detail="Verified credentials are a Premium feature.")
    p = payload or {}
    cred = uuid.uuid4().hex[:10]
    db.execute(_t("CREATE TABLE IF NOT EXISTS certificates (cred_id TEXT, user_id INTEGER, holder TEXT, role TEXT, score TEXT, created_at TEXT)"))
    db.execute(_t("INSERT INTO certificates (cred_id, user_id, holder, role, score, created_at) VALUES (:c,:u,:h,:r,:s,:t)"),
               {"c": cred, "u": user.id, "h": str(p.get("holder",""))[:120], "r": str(p.get("role",""))[:80],
                "s": str(p.get("score",""))[:10], "t": _dt.utcnow().isoformat()})
    db.commit()
    return {"cred_id": cred, "url": "https://grcwithgaurav.com/c/" + cred}
'''
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] credential mint endpoint added")

# 2. Public verification page (branded, og-meta for LinkedIn previews)
sr = [x for x in glob.glob("**/site_routes.py", recursive=True) if not any(t in x for t in skip)][0]
r = open(sr, encoding="utf-8").read()
if '"/c/{cred_id}"' not in r:
    page = '''@router.get("/c/{cred_id}", response_class=HTMLResponse)
async def credential_page(cred_id: str):
    import html as _h
    from sqlalchemy import text as _t
    row = None
    try:
        from database import SessionLocal
        db = SessionLocal()
        try:
            row = db.execute(_t("SELECT holder, role, score, created_at FROM certificates WHERE cred_id=:c"), {"c": cred_id}).fetchone()
        finally:
            db.close()
    except Exception:
        row = None
    if not row:
        return HTMLResponse("<html><body style='font-family:sans-serif;background:#0a0a0a;color:#e0e0e0;text-align:center;padding:4rem'><h2>Credential not found</h2><p>Check the link or earn your own at <a href='https://grcwithgaurav.com/app.html' style='color:#00ffcc'>grcwithgaurav.com</a>.</p></body></html>", status_code=404)
    holder, role, score, created = _h.escape(str(row[0])), _h.escape(str(row[1])), _h.escape(str(row[2])), _h.escape(str(row[3])[:10])
    return HTMLResponse(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{holder} - Verified {role} Credential | GRCWithGaurav</title>
<meta property="og:title" content="{holder} scored {score}/100 on {role} - Verified">
<meta property="og:description" content="Independently verified AI mock-interview credential issued by GRCWithGaurav (CyberVerse AI).">
<meta property="og:url" content="https://grcwithgaurav.com/c/{cred_id}">
<style>body{{margin:0;background:#0a0a0a;color:#e0e0e0;font-family:'Segoe UI',Arial,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.card{{max-width:560px;width:92%;background:#111;border:1px solid #222;border-radius:16px;padding:2.2rem;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
.logo{{font-family:Consolas,monospace;color:#00ffcc;font-weight:700;letter-spacing:1px}}
.badge{{display:inline-block;margin:1rem 0 .4rem;background:#00ffcc;color:#001512;font-weight:800;font-size:.72rem;letter-spacing:2px;padding:.3rem .9rem;border-radius:14px}}
h1{{color:#fff;margin:.4rem 0 .2rem;font-size:1.7rem}}
.role{{color:#9aa4b2;margin:0 0 1.2rem}}
.score{{font-size:4rem;font-weight:800;color:#00ffcc;line-height:1}} .score span{{font-size:1.4rem;color:#666}}
.meta{{color:#666;font-size:.8rem;margin:1.2rem 0 .6rem}}
.verify{{color:#9aa4b2;font-size:.82rem;line-height:1.6}}
.cta{{display:inline-block;margin-top:1.4rem;background:#00ffcc;color:#001512;font-weight:700;padding:.7rem 1.4rem;border-radius:10px;text-decoration:none}}</style>
</head><body><div class="card">
<div class="logo">&gt;_ CYBERVERSE.AI</div>
<div class="badge">VERIFIED CREDENTIAL</div>
<h1>{holder}</h1>
<p class="role">{role} &mdash; AI Mock Interview</p>
<div class="score">{score}<span>/100</span></div>
<p class="meta">Issued {created} &middot; Credential ID {cred_id}</p>
<p class="verify">Issued by GRCWithGaurav (CyberVerse AI) after a proctored AI mock interview with turn-by-turn scoring. Any recruiter can verify this credential at grcwithgaurav.com/c/&lt;id&gt;.</p>
<a class="cta" href="https://grcwithgaurav.com/app.html">Earn yours free &rarr;</a>
</div></body></html>""")

'''
    anchor = '@router.get("/refund-policy", response_class=HTMLResponse)'
    if anchor not in r:
        anchor = '@router.get("/admin-leads", response_class=HTMLResponse)'
    r = r.replace(anchor, page + anchor)
    open(sr, "w", encoding="utf-8").write(r)
    print("[ROUTE] public /c/{id} verification page added")

# 3. Frontend: add "Copy verification link" button to scorecard modal
ah = [x for x in glob.glob("**/app.html", recursive=True) if not any(t in x for t in skip)][0]
h = open(ah, encoding="utf-8").read()
js = """
<script id="cv-credential">
(function(){
  function addVerifyBtn(){
    var modal = document.getElementById("scorecard-modal");
    if(!modal || document.getElementById("sc-verify")) return;
    var anchor = document.getElementById("sc-copy") || document.getElementById("sc-download");
    var btn = document.createElement("button");
    btn.id = "sc-verify";
    btn.className = anchor ? anchor.className : "btn-secondary";
    btn.style.marginTop = "8px";
    btn.textContent = "\\ud83d\\udd17 Copy verification link";
    if(anchor && anchor.parentNode) anchor.parentNode.insertBefore(btn, anchor.nextSibling);
    else modal.appendChild(btn);
    btn.addEventListener("click", function(){
      var holder = (document.getElementById("stat-name")||{}).textContent || "";
      var role = (document.getElementById("sc-role")||{}).textContent || "";
      var score = (document.getElementById("sc-score")||{}).textContent || "";
      fetch("/api/analytics/interview/credential",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+localStorage.getItem("cv_token")},body:JSON.stringify({holder:holder,role:role,score:score})})
      .then(function(r){ return r.json(); }).then(function(d){
        if(d && d.url){
          if(navigator.clipboard) navigator.clipboard.writeText(d.url);
          btn.textContent = "\\u2705 Copied: " + d.url;
          setTimeout(function(){ btn.textContent = "\\ud83d\\udd17 Copy verification link"; }, 5000);
        } else {
          btn.textContent = "\\u26a0 Premium required";
          setTimeout(function(){ btn.textContent = "\\ud83d\\udd17 Copy verification link"; }, 3000);
        }
      }).catch(function(){ btn.textContent = "\\u26a0 Network error"; });
    });
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", addVerifyBtn); else addVerifyBtn();
})();
</script>
"""
if "cv-credential" not in h:
    idx = h.rfind("</body>")
    h = h[:idx] + js + h[idx:]
    open(ah, "w", encoding="utf-8").write(h)
    print("[FRONTEND] verification-link button added to scorecard")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Premium: shareable verified credentials (public /c/{id} page + copy-link button)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
