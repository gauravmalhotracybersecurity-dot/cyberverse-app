import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from claude_client import call_claude_json, ClaudeClientError
from config import settings
from database import get_db
from prompts import daily_bundle_system_prompt
from rate_limit import limiter

router = APIRouter(prefix="/api/daily", tags=["daily"])


def _today() -> str:
    return dt.date.today().isoformat()


def _update_streak(user: models.User, today: str):
    if user.last_active_date == today:
        return
    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    user.streak_days = user.streak_days + 1 if user.last_active_date == yesterday else 1
    user.last_active_date = today


@router.get("", response_model=schemas.DailyBundleResponse)
@limiter.limit(settings.rate_limit_daily)
async def get_today_bundle(
    request: Request,
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

    bundle = models.DailyBundle(user_id=user.id, date=today, content=content)
    db.add(bundle)

    _update_streak(user, today)
    user.xp += 10
    db.commit()

    return schemas.DailyBundleResponse(date=today, content=content)
