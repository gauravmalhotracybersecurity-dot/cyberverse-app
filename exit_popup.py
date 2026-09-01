import re, glob, os

htmls = [f for f in glob.glob("**/*.html", recursive=True)
         if not any(x in f for x in ("venv","node_modules",".git"))]

popup = """
<!-- CV EXIT-INTENT POPUP -->
<div id="cv-exit" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:99999;align-items:center;justify-content:center;">
  <div style="background:#0d0d0d;border:1px solid #00ffcc;border-radius:14px;max-width:440px;width:92%;padding:28px;position:relative;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.6);">
    <button id="cv-exit-x" style="position:absolute;top:10px;right:12px;background:none;border:none;color:#888;font-size:20px;cursor:pointer;">X</button>
    <div style="font-size:1.35rem;font-weight:800;color:#fff;line-height:1.25;">Wait - your resume is <span style="color:#00ffcc">6 seconds</span> from being rejected.</div>
    <p style="color:#bbb;font-size:.92rem;margin:12px 0 18px;">Get your <strong style="color:#fff">FREE AI Resume Score</strong> + the exact bullets to fix before you go.</p>
    <form id="cv-exit-form" style="display:flex;flex-direction:column;gap:10px;">
      <input id="cv-exit-email" type="email" required placeholder="you@domain.com" style="padding:12px;border-radius:8px;border:1px solid #333;background:#151515;color:#fff;font-size:.95rem;outline:none;">
      <button type="submit" style="padding:12px;border-radius:8px;border:none;background:#00ffcc;color:#001512;font-weight:800;font-size:1rem;cursor:pointer;">Score My Resume Free</button>
    </form>
    <div style="color:#666;font-size:.75rem;margin-top:10px;">No spam. Just your score + fixes.</div>
  </div>
</div>
<script id="cv-exit-js">
(function(){
  var shown = sessionStorage.getItem('cvExitShown');
  var box = document.getElementById('cv-exit');
  function show(){
    if (shown) return;
    shown = 1; sessionStorage.setItem('cvExitShown','1');
    box.style.display = 'flex';
  }
  document.addEventListener('mouseout', function(e){
    if (!e.relatedTarget && e.clientY <= 0) show();
  });
  if ('ontouchstart' in window) setTimeout(show, 40000);
  document.getElementById('cv-exit-x').addEventListener('click', function(){ box.style.display='none'; });
  box.addEventListener('click', function(e){ if (e.target === box) box.style.display='none'; });
  document.getElementById('cv-exit-form').addEventListener('submit', function(e){
    e.preventDefault();
    var em = document.getElementById('cv-exit-email').value.trim();
    if (!em) return;
    fetch('/api/analytics/lead', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email: em})}).catch(function(){});
    location.href = '/app.html?email=' + encodeURIComponent(em) + '&mode=signup';
  });
})();
</script>
"""

prefill = """
<script id="cv-prefill">
(function(){
  var p = new URLSearchParams(location.search);
  var em = p.get('email');
  if (!em) return;
  function pre(){
    var tab = document.querySelector('[data-mode="signup"]');
    if (tab) tab.click();
    setTimeout(function(){
      var inp = document.querySelector('input[type="email"]');
      if (inp) inp.value = em;
    }, 300);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pre); else pre();
})();
</script>
"""

for f in htmls:
    s = open(f, encoding='utf-8').read()
    changed = False
    if f.endswith('index.html') and 'cv-exit' not in s:
        s = s.replace('</body>', popup + '\n</body>'); changed = True
        print('[INJECTED] exit-intent popup ->', f)
    if f.endswith('app.html') and 'cv-prefill' not in s:
        s = s.replace('</body>', prefill + '\n</body>'); changed = True
        print('[INJECTED] email prefill ->', f)
    if changed:
        open(f, 'w', encoding='utf-8').write(s)

backend_code = """

@router.post("/lead")
def capture_lead(payload: dict, db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    from datetime import datetime as _dt
    try:
        db.execute(_text("CREATE TABLE IF NOT EXISTS leads (email TEXT, created_at TEXT)"))
        db.execute(_text("INSERT INTO leads (email, created_at) VALUES (:e, :t)"),
                   {"e": (payload or {}).get("email", ""), "t": _dt.utcnow().isoformat()})
        db.commit()
    except Exception:
        pass
    return {"ok": True}


@router.get("/leads")
def list_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text as _text
    try:
        rows = db.execute(_text("SELECT email, created_at FROM leads ORDER BY created_at DESC LIMIT 200")).fetchall()
    except Exception:
        rows = []
    return [{"email": r[0], "created_at": r[1]} for r in rows]
"""

ar = [f for f in glob.glob("backend/routers/analytics_routes.py")]
if ar:
    s = open(ar[0], encoding='utf-8').read()
    if 'def capture_lead' not in s:
        open(ar[0], 'w', encoding='utf-8').write(s + backend_code)
        print('[BACKEND] /api/analytics/lead + /leads endpoints added')

os.system('git add -A')
os.system('git commit -m "Growth: exit-intent popup capturing emails for free resume score"')
os.system('git push origin main')
print('Pushed. Live in ~60s.')
