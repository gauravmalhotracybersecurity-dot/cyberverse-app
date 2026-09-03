import os, json
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
import sys

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
    # Redirects to homepage until Careers pages are built in a future phase
    return RedirectResponse(url="/", status_code=302)

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
    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b"] + TOOL_PATHS + ["/learn/" + a["slug"] for a in ARTICLES]
    items = ""
    for p in paths:
        items += "<url><loc>" + BASE_URL + p + "</loc><lastmod>2026-09-03</lastmod><changefreq>weekly</changefreq></url>"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>"
    return Response(xml, media_type="application/xml")

@router.get("/robots.txt")
async def robots():
    txt = "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin.html\nDisallow: /app.html\n\nSitemap: " + BASE_URL + "/sitemap.xml\n"
    return Response(txt, media_type="text/plain")
