from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from claude_client import call_claude_json, ClaudeClientError
from config import settings
from database import get_db
from prompts import interview_system_prompt
from rate_limit import limiter

router = APIRouter(prefix="/api/interview", tags=["interview"])

MAX_TURNS = 6


def _history_as_messages(session: models.InterviewSession) -> list[dict]:
    """Reconstruct the conversation for Claude: interviewer asks, candidate answers."""
    msgs = []
    for turn in session.turns:
        role = "assistant" if turn.speaker == "interviewer" else "user"
        msgs.append({"role": role, "content": turn.content})
    return msgs


@router.post("/start", response_model=schemas.InterviewStartResponse)
@limiter.limit(settings.rate_limit_interview)
async def start_interview(
    request: Request,
    payload: schemas.InterviewStartRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = models.InterviewSession(user_id=user.id, role=payload.role, status="active")
    db.add(session)
    db.flush()

    try:
        result = await call_claude_json(
            system=interview_system_prompt(payload.role),
            messages=[{"role": "user", "content": "Begin the interview with your first question."}],
            max_tokens=800,
        )
    except ClaudeClientError as e:
        db.rollback()
        raise HTTPException(status_code=502, detail=str(e))

    first_question = result.get("next_question") or "Tell me about yourself and your background in security."
    turn = models.InterviewTurn(session_id=session.id, speaker="interviewer", content=first_question)
    db.add(turn)
    db.commit()
    db.refresh(session)

    return schemas.InterviewStartResponse(session_id=session.id, role=session.role, turns=session.turns)


@router.post("/{session_id}/respond", response_model=schemas.InterviewRespondResponse)
@limiter.limit(settings.rate_limit_interview)
async def respond(
    request: Request,
    session_id: int,
    payload: schemas.InterviewRespondRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.InterviewSession)
        .filter(models.InterviewSession.id == session_id, models.InterviewSession.user_id == user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="This interview has already ended.")

    candidate_turn = models.InterviewTurn(
        session_id=session.id, speaker="candidate", content=payload.answer
    )
    db.add(candidate_turn)
    db.flush()

    answered_count = sum(1 for t in session.turns if t.speaker == "candidate")
    force_wrap_up = answered_count >= MAX_TURNS

    history_messages = _history_as_messages(session)
    instruction = (
        "The candidate just answered. Evaluate their answer, then, since this was the "
        f"final question ({MAX_TURNS} answered), set is_complete true and give closing_remarks."
        if force_wrap_up
        else "The candidate just answered. Evaluate their answer, then ask the next question."
    )
    history_messages.append({"role": "user", "content": instruction})

    try:
        result = await call_claude_json(
            system=interview_system_prompt(session.role),
            messages=history_messages,
            max_tokens=900,
        )
    except ClaudeClientError as e:
        db.rollback()
        raise HTTPException(status_code=502, detail=str(e))

    candidate_turn.feedback = result.get("feedback")

    is_complete = bool(result.get("is_complete")) or force_wrap_up
    if is_complete:
        session.status = "completed"
        closing = result.get("closing_remarks") or "Interview complete. Nice work."
        db.add(models.InterviewTurn(session_id=session.id, speaker="interviewer", content=closing))
        user.xp += 25
    else:
        next_q = result.get("next_question") or "Can you walk me through your reasoning further?"
        db.add(models.InterviewTurn(session_id=session.id, speaker="interviewer", content=next_q))
        user.xp += 5

    db.commit()
    db.refresh(session)

    return schemas.InterviewRespondResponse(
        session_id=session.id, turns=session.turns, is_complete=is_complete
    )
