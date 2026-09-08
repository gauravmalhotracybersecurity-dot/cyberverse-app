import glob, subprocess
skip = ("venv", "node_modules", ".git")
sr = [x for x in glob.glob("**/site_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(sr, encoding="utf-8").read()

verify_endpoint = '''

@router.get("/verify/{verify_id}")
def verify_certificate(verify_id: str, db: Session = Depends(get_db)):
    from sqlalchemy import text as _t
    import hashlib as _h
    # Find matching session
    rows = db.execute(_t("SELECT s.id, s.user_id, s.role, s.overall_score, s.created_at, u.full_name, u.email FROM interview_sessions s JOIN users u ON u.id = s.user_id WHERE s.status = 'completed' ORDER BY s.created_at DESC LIMIT 1000")).fetchall()
    for r in rows:
        session_id, user_id, role, score, created_at, full_name, email = r
        candidate_id = _h.sha256(f"{session_id}-{user_id}-{created_at}".encode()).hexdigest()[:12]
        if candidate_id == verify_id:
            name = full_name or email.split("@")[0]
            from datetime import datetime as _dt
            date_str = created_at.strftime("%B %d, %Y") if hasattr(created_at, 'strftime') else str(created_at)
            return _render_verify_page(verify_id, name, role, score, date_str, valid=True)
    return _render_verify_page(verify_id, None, None, None, None, valid=False)

def _render_verify_page(verify_id, name, role, score, date_str, valid):
    if valid:
        html = f"""<!DOCTYPE html>
<html>
<head>
<title>Certificate Verified - CyberVerse AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 40px 20px; }}
.container {{ max-width: 600px; margin: 0 auto; background: #1a1a1a; border-radius: 12px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }}
.badge {{ display: inline-block; background: #00ffcc; color: #0a0a0a; padding: 8px 20px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-bottom: 20px; }}
h1 {{ color: #00ffcc; margin-top: 0; }}
.detail {{ margin: 20px 0; padding: 15px; background: #0a0a0a; border-left: 4px solid #00ffcc; }}
.label {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
.value {{ font-size: 18px; color: #fff; }}
.footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; font-size: 12px; color: #666; }}
</style>
</head>
<body>
<div class="container">
<div class="badge">✓ VERIFIED</div>
<h1>Certificate Authentication</h1>
<p>This certificate is authentic and was issued by CyberVerse AI.</p>
<div class="detail">
<div class="label">Issued To</div>
<div class="value">{name}</div>
</div>
<div class="detail">
<div class="label">Role</div>
<div class="value">{role} Mock Interview</div>
</div>
<div class="detail">
<div class="label">Score</div>
<div class="value">{score}/100</div>
</div>
<div class="detail">
<div class="label">Date Issued</div>
<div class="value">{date_str}</div>
</div>
<div class="detail">
<div class="label">Verification ID</div>
<div class="value" style="font-family: monospace; font-size: 14px;">{verify_id}</div>
</div>
<div class="footer">
This certificate was earned through demonstrated competency in AI-simulated interviews at <a href="https://app.grcwithgaurav.com" style="color:#00ffcc">app.grcwithgaurav.com</a>.
</div>
</div>
</body>
</html>"""
    else:
        html = """<!DOCTYPE html>
<html>
<head>
<title>Certificate Not Found - CyberVerse AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial, sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 40px 20px; }
.container { max-width: 600px; margin: 0 auto; background: #1a1a1a; border-radius: 12px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
.badge { display: inline-block; background: #ff4444; color: #fff; padding: 8px 20px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-bottom: 20px; }
h1 { color: #ff4444; margin-top: 0; }
.footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; font-size: 12px; color: #666; }
</style>
</head>
<body>
<div class="container">
<div class="badge">✗ NOT FOUND</div>
<h1>Certificate Not Found</h1>
<p>We could not find a certificate matching this verification ID.</p>
<p>This may be because:</p>
<ul>
<li>The verification ID is incorrect</li>
<li>The certificate has been revoked</li>
<li>The certificate was never issued</li>
</ul>
<div class="footer">
If you believe this is an error, contact <a href="mailto:hello@mail.grcwithgaurav.com" style="color:#00ffcc">hello@mail.grcwithgaurav.com</a>.
</div>
</div>
</body>
</html>"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html, status_code=200 if valid else 404)
'''

if '"/verify/' not in c:
    c += verify_endpoint
    print("[ADDED] certificate verification endpoint")
else:
    print("[SKIP] verify endpoint already exists")

try:
    compile(c, sr, "exec")
    open(sr, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Verification: /verify/{id} endpoint for certificate authenticity checks"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
