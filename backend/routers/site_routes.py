import os, json
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
import sys
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

# Import article database
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from content.articles import ARTICLES

# Flip to https://grcwithgaurav.com when the main domain DNS is migrated to Render
BASE_URL = "https://grcwithgaurav.com"

TOOL_PATHS = [
    "/tools/iso-risk-calculator",
    "/tools/cvss-calculator",
    "/tools/iso-gap-assessment",
    "/tools/ats-resume-checker",
    "/tools/risk-register-generator",
    "/tools/security-policy-generator",
    "/tools/iso27001-control-finder",
    "/tools/incident-severity-calculator",
    "/tools/vendor-risk-assessment"
]

# Load books/ebooks
_BOOKS = []
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "books.json"), encoding="utf-8") as _bf:
        _BOOKS = json.load(_bf)
except Exception:
    _BOOKS = []

# ================= EXPLICIT ROUTES =================
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    return templates.TemplateResponse("resources.html", {"request": request, "books": _BOOKS})

@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/tools", response_class=HTMLResponse)
async def tools_index(request: Request):
    return templates.TemplateResponse("tools/index.html", {"request": request})

@router.get("/tools/iso-risk-calculator", response_class=HTMLResponse)
async def iso_risk_calculator(request: Request):
    return templates.TemplateResponse("tools/iso_risk_calculator.html", {"request": request})

@router.get("/tools/cvss-calculator", response_class=HTMLResponse)
async def cvss_calculator(request: Request):
    return templates.TemplateResponse("tools/cvss_calculator.html", {"request": request})

@router.get("/tools/iso-gap-assessment", response_class=HTMLResponse)
async def iso_gap_assessment(request: Request):
    return templates.TemplateResponse("tools/iso_gap_assessment.html", {"request": request})

@router.get("/tools/ats-resume-checker", response_class=HTMLResponse)
async def ats_resume_checker(request: Request):
    return templates.TemplateResponse("tools/ats_resume_checker.html", {"request": request})

@router.get("/tools/risk-register-generator", response_class=HTMLResponse)
async def risk_register_generator(request: Request):
    return templates.TemplateResponse("tools/risk_register_generator.html", {"request": request})

@router.get("/tools/security-policy-generator", response_class=HTMLResponse)
async def security_policy_generator(request: Request):
    return templates.TemplateResponse("tools/security_policy_generator.html", {"request": request})

@router.get("/tools/iso27001-control-finder", response_class=HTMLResponse)
async def iso27001_control_finder(request: Request):
    return templates.TemplateResponse("tools/iso27001_control_finder.html", {"request": request})

@router.get("/tools/incident-severity-calculator", response_class=HTMLResponse)
async def incident_severity_calculator(request: Request):
    return templates.TemplateResponse("tools/incident_severity_calculator.html", {"request": request})

@router.get("/tools/vendor-risk-assessment", response_class=HTMLResponse)
async def vendor_risk_assessment(request: Request):
    return templates.TemplateResponse("tools/vendor_risk_assessment.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
async def learn_index(request: Request):
    cats = {}
    for a in ARTICLES:
        cats.setdefault(a["category"], []).append(a)
    return templates.TemplateResponse("learn/index.html", {"request": request, "categories": cats})

@router.get("/learn/{slug}", response_class=HTMLResponse)
async def learn_article(request: Request, slug: str):
    art = next((a for a in ARTICLES if a["slug"] == slug), None)
    if not art:
        return RedirectResponse(url="/learn", status_code=302)
    return templates.TemplateResponse("learn/article.html", {"request": request, "article": art, "base_url": BASE_URL})

@router.get("/careers", response_class=HTMLResponse)
async def careers_page(request: Request):
    return templates.TemplateResponse("careers.html", {"request": request})

@router.get("/c/{cred_id}", response_class=HTMLResponse)
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

@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@router.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer_page(request: Request):
    return templates.TemplateResponse("disclaimer.html", {"request": request})

@router.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy_page(request: Request):
    return templates.TemplateResponse("refunds.html", {"request": request})

@router.get("/admin-payments", response_class=HTMLResponse)
async def admin_payments_page(request: Request):
    return templates.TemplateResponse("admin_payments.html", {"request": request})

@router.get("/admin-leads", response_class=HTMLResponse)
async def admin_leads_page(request: Request):
    return templates.TemplateResponse("admin_leads.html", {"request": request})

@router.get("/b2b", response_class=HTMLResponse)
async def b2b_page(request: Request):
    return templates.TemplateResponse("b2b.html", {"request": request})

# ================= 301 REDIRECT MAP =================
_REDIRECTS = {"/books": "/resources", "/consulting": "/b2b", "/blog": "/learn", "/home": "/", "/about-us": "/about"}
def _make_redir(target):
    async def _r(request: Request):
        return RedirectResponse(url=target, status_code=301)
    return _r
for _old, _new in _REDIRECTS.items():
    router.add_api_route(_old, _make_redir(_new), methods=["GET"], include_in_schema=False)

# ================= SEO =================
@router.get("/sitemap.xml")
async def sitemap():
    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b", "/careers", "/faq"] + TOOL_PATHS + ["/learn/" + a["slug"] for a in ARTICLES]
    seen = set()
    items = ""
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        lm = "2026-09-11"
        for a in ARTICLES:
            if p == "/learn/" + a["slug"]:
                lm = a.get("date", "2026-09-11")
                break
        items += "<url><loc>" + BASE_URL + p + "</loc><lastmod>" + lm + "</lastmod><changefreq>weekly</changefreq></url>"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>"
    return Response(xml, media_type="application/xml")

@router.get("/robots.txt")
async def robots():
    txt = "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin.html\nDisallow: /app.html\nDisallow: /admin-payments\nDisallow: /admin-leads\n\nSitemap: " + BASE_URL + "/sitemap.xml\n"
    return Response(txt, media_type="text/plain")


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


@router.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})
