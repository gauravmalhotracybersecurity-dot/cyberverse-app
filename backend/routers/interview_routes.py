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
from weak_topics import merge_weak_topics

router = APIRouter(prefix="/api/interview", tags=["interview"])

MAX_TURNS = 6


def _history_as_messages(session: models.InterviewSession) -> list[dict]:
    """Reconstruct the conversation for Claude: interviewer asks, candidate answers."""
    msgs = []
    for turn in session.turns:
        role = "assistant" if turn.speaker == "interviewer" else "user"
        msgs.append({"role": role, "content": turn.content})
    return msgs


def _get_past_questions(user_id: int, db: Session, limit: int = 10) -> list[str]:
    turns = (
        db.query(models.InterviewTurn.content)
        .join(models.InterviewSession)
        .filter(
            models.InterviewSession.user_id == user_id,
            models.InterviewTurn.speaker == "interviewer"
        )
        .order_by(models.InterviewTurn.id.desc())
        .limit(limit)
        .all()
    )
    return [t[0] for t in turns]


@router.get("/active")
async def get_active_interview(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.InterviewSession)
        .filter(models.InterviewSession.user_id == user.id, models.InterviewSession.status == "active")
        .order_by(models.InterviewSession.created_at.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="No active session.")
    return {"session_id": session.id, "role": session.role, "turns": [{"speaker": t.speaker, "content": t.content, "feedback": t.feedback} for t in session.turns]}
@router.post("/start", response_model=schemas.InterviewStartResponse)
@limiter.limit(settings.rate_limit_interview)
async def start_interview(
    request: Request,
    payload: schemas.InterviewStartRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if not user.is_pro:
        total_sessions = db.query(models.InterviewSession).filter(models.InterviewSession.user_id == user.id).count()
        if total_sessions >= 3:
            raise HTTPException(status_code=403, detail="Free tier limit reached (3 interviews). Upgrade to Pro for unlimited mock interviews.")
    session = models.InterviewSession(user_id=user.id, role=payload.role, status="active")
    db.add(session)
    db.flush()

    try:
        result = await call_claude_json(
            system=interview_system_prompt(payload.role, _get_past_questions(user.id, db)),
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
        f"final question ({MAX_TURNS} answered), set is_complete true, give closing_remarks, an overall_score (integer 0-100), and a one-line verdict."
        if force_wrap_up
        else "The candidate just answered. Evaluate their answer, then ask the next question."
    )
    history_messages.append({"role": "user", "content": instruction})

    try:
        result = await call_claude_json(
            system=interview_system_prompt(session.role, _get_past_questions(user.id, db)),
            messages=history_messages,
            max_tokens=900,
        )
    except ClaudeClientError as e:
        db.rollback()
        raise HTTPException(status_code=502, detail=str(e))

    candidate_turn.feedback = result.get("feedback")
    merge_weak_topics(user, result.get("weak_topics"))

    is_complete = bool(result.get("is_complete")) or force_wrap_up
    if is_complete:
        session.status = "completed"
        session.overall_score = result.get("overall_score")
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
        session_id=session.id, turns=session.turns, is_complete=is_complete,
        overall_score=session.overall_score, verdict=result.get("verdict"), role=session.role
    )
