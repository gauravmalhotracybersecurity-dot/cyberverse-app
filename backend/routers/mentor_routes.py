from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from claude_client import call_claude, ClaudeClientError
from config import settings
from database import get_db
from prompts import mentor_system_prompt
from rate_limit import limiter

router = APIRouter(prefix="/api/mentor", tags=["mentor"])

HISTORY_WINDOW = 20  # last N messages sent to the model as short-term memory


@router.get("/history", response_model=list[schemas.ChatMessageOut])
def get_history(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    msgs = (
        db.query(models.MentorMessage)
        .filter(models.MentorMessage.user_id == user.id)
        .order_by(models.MentorMessage.created_at.asc())
        .all()
    )
    return msgs


@router.post("/chat", response_model=schemas.ChatResponse)
@limiter.limit(settings.rate_limit_chat)
async def chat(
    request: Request,
    payload: schemas.ChatRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Load recent history for short-term conversational memory
    recent = (
        db.query(models.MentorMessage)
        .filter(models.MentorMessage.user_id == user.id)
        .order_by(models.MentorMessage.created_at.desc())
        .limit(HISTORY_WINDOW)
        .all()
    )
    recent.reverse()

    claude_messages = [{"role": m.role, "content": m.content} for m in recent]
    claude_messages.append({"role": "user", "content": payload.message})

    try:
        reply = await call_claude(
            system=mentor_system_prompt(user),
            messages=claude_messages,
            max_tokens=1024,
        )
    except ClaudeClientError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # Persist both sides of the exchange
    user_msg = models.MentorMessage(user_id=user.id, role="user", content=payload.message)
    assistant_msg = models.MentorMessage(user_id=user.id, role="assistant", content=reply)
    db.add_all([user_msg, assistant_msg])

    # Light gamification: award XP for engaging with the mentor
    user.xp += 5
    db.commit()

    full_history = (
        db.query(models.MentorMessage)
        .filter(models.MentorMessage.user_id == user.id)
        .order_by(models.MentorMessage.created_at.asc())
        .all()
    )
    return schemas.ChatResponse(reply=reply, history=full_history)
