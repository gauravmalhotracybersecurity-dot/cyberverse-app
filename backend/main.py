import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from config import settings
from database import Base, engine
from rate_limit import limiter
from routers import (
    achievement_routes,
    auth_routes,
    profile_routes,
    mentor_routes,
    daily_routes,
    resume_routes,
    interview_routes,
)

logging.basicConfig(
    level=logging.INFO if settings.environment == "production" else logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("cyberverse")

# On first run this creates tables directly. Once you're running migrations
# (see alembic/), remove this line and rely on `alembic upgrade head` instead
# so schema changes are tracked. Left in place for zero-friction local dev.
if settings.environment != "production":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberVerse AI API", version="0.2.0")

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "You're doing that too often. Please slow down and try again shortly."},
    )


# CORS only matters when the frontend is served from a different origin than
# the API (e.g. a split deployment). When FastAPI serves the frontend itself
# (see the StaticFiles mount below), requests are same-origin and this is
# effectively unused - it's kept so a split deployment still works out of
# the box by setting ALLOWED_ORIGINS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


app.include_router(auth_routes.router)
app.include_router(achievement_routes.router)
app.include_router(profile_routes.router)
app.include_router(mentor_routes.router)
app.include_router(daily_routes.router)
app.include_router(resume_routes.router)
app.include_router(interview_routes.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "environment": settings.environment}


# Serve the frontend from the same origin/process when its build output is
# present. This is what the Docker image does (see Dockerfile). Must be
# mounted last, after all /api routes, so it only catches what they don't.
if settings.frontend_dir and os.path.isdir(settings.frontend_dir):
    app.mount("/", StaticFiles(directory=settings.frontend_dir, html=True), name="frontend")
    logger.info("Serving frontend from %s", settings.frontend_dir)
else:
    logger.info("No frontend_dir found - API-only mode (serve the frontend separately).")
