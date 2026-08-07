import datetime as dt
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from claude_client import call_claude_json, ClaudeClientError
from config import settings
from database import get_db
from email_service import send_email
from prompts import daily_bundle_system_prompt
from rate_limit import limiter

logger = logging.getLogger("cyberverse.daily")

router = APIRouter(prefix="/api/daily", tags=["daily"])


def _today() -> str:
    return dt.date.today().isoformat()


def _update_streak(user: models.User, today: str):
    if user.last_active_date == today:
        return
    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    user.streak_days = user.streak_days + 1 if user.last_active_date == yesterday else 1
    user.last_active_date = today


def _bundle_email_body(name, date, content, streak):
    topic = content.get("lesson_topic") or "Your daily cyber lesson"
    subject = "[CyberVerse] Day " + str(streak) + " - " + str(topic)[:40] + " - don't break your streak"
    base = settings.app_base_url.rstrip("/")
    body = (
        "Hey " + (name or "Operator") + ", your CyberVerse daily bundle for " + date + " is ready.\n\n"
        "Lesson: " + str(content.get("lesson_topic", "")) + "\n"
        + str(content.get("lesson", ""))[:600] + "\n\n"
        "Challenge: " + str(content.get("challenge", "")) + "\n"
        "Interview Q: " + str(content.get("interview_question", "")) + "\n\n"
        "You're on a " + str(streak) + "-day streak. Keep it alive:\n"
        + base + "/\n\n"
        "- Your CyberVerse AI mentor"
    )
    return subject, body


def _send_daily_email(to, name, date, content, streak):
    try:
        subject, body = _bundle_email_body(name, date, content, streak)
        send_email(to, subject, body)
    except Exception:
        logger.exception("Background daily email failed for %s", to)


@router.get("", response_model=schemas.DailyBundleResponse)
@limiter.limit(settings.rate_limit_daily)
async def get_today_bundle(
    request: Request,
    background_tasks: BackgroundTasks,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = _today()
    existing = (
        db.query(models.DailyBundle)
        .filter(models.DailyBundle.user_id == user.id, models.DailyBundle.date == today)
        .first()
    )
    if existing:
        return schemas.DailyBundleResponse(date=today, content=existing.content)

    try:
        content = await call_claude_json(
            system=daily_bundle_system_prompt(user),
            messages=[{"role": "user", "content": "Generate today's learning bundle."}],
            max_tokens=1800,
        )
    except ClaudeClientError as e:
        raise HTTPException(status_code=502, detail=str(e))

    _update_streak(user, today)
    user.xp += 10

    bundle = models.DailyBundle(user_id=user.id, date=today, content=content)
    db.add(bundle)
    db.flush()

    bundle.emailed_at = dt.datetime.utcnow()
    background_tasks.add_task(_send_daily_email, user.email, user.full_name, today, content, user.streak_days)

    db.commit()
    return schemas.DailyBundleResponse(date=today, content=content)


@router.post("/cron/send-briefs")
def cron_send_daily_briefs(
    cron_secret: str = Header(..., alias="x-cron-secret"),
    db: Session = Depends(get_db),
):
    if cron_secret != settings.jwt_secret:
        raise HTTPException(status_code=401, detail="Bad cron secret")

    today = _today()
    pending = (
        db.query(models.DailyBundle)
        .filter(models.DailyBundle.date == today, models.DailyBundle.emailed_at.is_(None))
        .all()
    )

    sent = 0
    for bundle in pending:
        user = db.get(models.User, bundle.user_id)
        if not user:
            continue
        try:
            subject, body = _bundle_email_body(user.full_name, today, bundle.content, user.streak_days)
            send_email(user.email, subject, body)
            bundle.emailed_at = dt.datetime.utcnow()
            db.commit()
            sent += 1
        except Exception:
            db.rollback()
            logger.exception("Cron send failed for user %s", bundle.user_id)

    return {"date": today, "pending": len(pending), "sent": sent}
