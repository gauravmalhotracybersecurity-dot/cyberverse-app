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
    admin_routes,
    achievement_routes,
    payment_routes,
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
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.include_router(auth_routes.router)
app.include_router(achievement_routes.router)
app.include_router(admin_routes.router)
app.include_router(payment_routes.router)
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

from fastapi.responses import FileResponse

@app.get("/app", include_in_schema=False)
def serve_app():
    return FileResponse("frontend/app.html")

def _ensure_extra_columns():
    try:
        from sqlalchemy import text
        from database import engine
        import models as _m
        t = _m.InterviewSession.__table__.name
        with engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS overall_score integer;\nALTER TABLE {t} ADD COLUMN IF NOT EXISTS nudge_sent_at timestamp;\nALTER TABLE {t} ADD COLUMN IF NOT EXISTS created_at timestamp DEFAULT CURRENT_TIMESTAMP;"))
            u = _m.User.__table__.name
            conn.execute(text(f"ALTER TABLE {u} ADD COLUMN IF NOT EXISTS is_verified boolean NOT NULL DEFAULT true;\nALTER TABLE {u} ADD COLUMN IF NOT EXISTS reset_nonce varchar;\nALTER TABLE {u} ADD COLUMN IF NOT EXISTS verify_nonce varchar;"))
            conn.commit()
    except Exception as e:
        import logging
        logging.getLogger("cyberverse").warning("startup migration skipped: %s", e)

_ensure_extra_columns()


import threading, time
from datetime import datetime, timedelta
from database import SessionLocal
from email_service import send_interview_nudge_email
import logging

def _nudge_loop():
    time.sleep(60) # wait 1 min after startup
    logging.getLogger("cyberverse").info("Nudge loop started.")
    while True:
        time.sleep(1800) # check every 30 minutes
        db = SessionLocal()
        try:
            cutoff = datetime.utcnow() - timedelta(hours=2)
            max_age = datetime.utcnow() - timedelta(hours=48) # don't nag for week-old sessions
            abandoned = db.query(models.InterviewSession).filter(
                models.InterviewSession.status == "active",
                models.InterviewSession.created_at < cutoff,
                models.InterviewSession.created_at > max_age,
                models.InterviewSession.nudge_sent_at == None
            ).all()
            for sess in abandoned:
                user = db.query(models.User).filter(models.User.id == sess.user_id).first()
                if user:
                    send_interview_nudge_email(user.email, user.full_name or "there", sess.role)
                    sess.nudge_sent_at = datetime.utcnow()
            db.commit()
        except Exception as e:
            logging.getLogger("cyberverse").error(f"Nudge loop error: {e}")
        finally:
            db.close()

threading.Thread(target=_nudge_loop, daemon=True).start()


def _ensure_streak_freeze_column():
    try:
        from sqlalchemy import text
        from database import engine
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS streak_freeze_used_today boolean DEFAULT false;"))
            conn.commit()
    except Exception as e:
        import logging
        logging.getLogger("cyberverse").warning("streak freeze migration skipped: %s", e)

_ensure_streak_freeze_column()


def _ensure_nurture_columns():
    try:
        from sqlalchemy import text
        from database import engine
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS day3_email_sent_at timestamp;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS day7_email_sent_at timestamp;"))
            conn.commit()
    except Exception as e:
        import logging
        logging.getLogger("cyberverse").warning("nurture columns migration skipped: %s", e)

_ensure_nurture_columns()


def _nurture_loop():
    time.sleep(120) # wait 2 min after startup
    logging.getLogger("cyberverse").info("Nurture loop started.")
    while True:
        time.sleep(3600 * 6) # check every 6 hours
        db = SessionLocal()
        try:
            from datetime import datetime, timedelta
            now = datetime.utcnow()
            
            # Day 3: signed up 3 days ago, never returned
            day3_cutoff = now - timedelta(days=3)
            day3_max = now - timedelta(days=4) # don't spam old accounts
            day3_users = db.query(models.User).filter(
                models.User.created_at < day3_cutoff,
                models.User.created_at > day3_max,
                models.User.is_verified == True,
                models.User.last_active_date == None,
                models.User.day3_email_sent_at == None
            ).all()
            
            for user in day3_users:
                unfinished = db.query(models.InterviewSession).filter(
                    models.InterviewSession.user_id == user.id,
                    models.InterviewSession.status == "active"
                ).count()
                send_day3_nurture_email(user.email, user.full_name or "there", user.weak_topics or [], unfinished)
                user.day3_email_sent_at = now
            
            # Day 7: signed up 7 days ago, minimal activity
            day7_cutoff = now - timedelta(days=7)
            day7_max = now - timedelta(days=8)
            day7_users = db.query(models.User).filter(
                models.User.created_at < day7_cutoff,
                models.User.created_at > day7_max,
                models.User.is_verified == True,
                models.User.xp < 50, # low engagement
                models.User.day7_email_sent_at == None
            ).all()
            
            for user in day7_users:
                # Try to find their resume score if they did a review
                resume_score = None
                from sqlalchemy import text
                try:
                    result = db.execute(text("SELECT overall_score FROM resume_reviews WHERE user_id = :uid ORDER BY id DESC LIMIT 1"), {"uid": user.id})
                    row = result.fetchone()
                    if row: resume_score = row[0]
                except: pass
                send_day7_nurture_email(user.email, user.full_name or "there", resume_score, user.xp)
                user.day7_email_sent_at = now
            
            db.commit()
        except Exception as e:
            logging.getLogger("cyberverse").error(f"Nurture loop error: {e}")
        finally:
            db.close()

threading.Thread(target=_nurture_loop, daemon=True).start()
