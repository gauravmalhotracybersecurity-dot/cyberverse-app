from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/learn", response_class=HTMLResponse)
@router.get("/tools", response_class=HTMLResponse)
@router.get("/careers", response_class=HTMLResponse)
@router.get("/resources", response_class=HTMLResponse)
async def placeholders(request: Request):
    # Simple placeholder for now so nav links don't 404
    return templates.TemplateResponse("index.html", {"request": request})
