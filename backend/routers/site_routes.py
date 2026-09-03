from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/tools", response_class=HTMLResponse)
async def tools_index(request: Request):
    return templates.TemplateResponse("tools/index.html", {"request": request})

@router.get("/tools/iso-risk-calculator", response_class=HTMLResponse)
async def iso_risk_calculator(request: Request):
    return templates.TemplateResponse("tools/iso_risk_calculator.html", {"request": request})

@router.get("/tools/cvss-calculator", response_class=HTMLResponse)
async def cvss_calculator(request: Request):
    return templates.TemplateResponse("tools/cvss_calculator.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
@router.get("/careers", response_class=HTMLResponse)
@router.get("/resources", response_class=HTMLResponse)
async def placeholders(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
