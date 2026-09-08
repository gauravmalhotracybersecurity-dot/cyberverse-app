from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
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
        if total_sessions >= (3 + (user.bonus_interviews or 0)):
            raise HTTPException(status_code=403, detail="Free tier limit reached (3 interviews). Upgrade to Pro for unlimited mock interviews.")
    session = models.InterviewSession(user_id=user.id, role=payload.role, status="active", max_turns=3 if payload.quick else 6)
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
    force_wrap_up = answered_count >= (session.max_turns or MAX_TURNS)

    history_messages = _history_as_messages(session)
    instruction = (
        "The candidate just answered. Evaluate their answer, then, since this was the "
        f"final question ({(session.max_turns or MAX_TURNS)} answered), set is_complete true, give closing_remarks, an overall_score (integer 0-100), and a one-line verdict."
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
    verdict_text = None
    if is_complete:
        session.status = "completed"
        closing = result.get("closing_remarks") or "Interview complete. Nice work."
        # score parsing v2
        session.overall_score = result.get("overall_score")
        if session.overall_score is None:
            import re as _re
            _m = _re.search(r"(\d{1,3})\s*/\s*100", closing)
            if _m:
                session.overall_score = int(_m.group(1))
        if session.overall_score is None:
            _wt = result.get("weak_topics") or []
            session.overall_score = max(55, 95 - 10 * len(_wt))
        verdict_text = result.get("verdict") or ""
        if not verdict_text:
            verdict_text = (closing.split(". ")[0].strip() + ".")[:160]
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
        overall_score=session.overall_score, verdict=verdict_text, role=session.role
    )


@router.get("/{session_id}/certificate")
def get_certificate(session_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_premium:
        raise HTTPException(status_code=403, detail="Premium feature only. Upgrade to 999.")
    session = db.query(models.InterviewSession).filter(models.InterviewSession.id == session_id, models.InterviewSession.user_id == user.id).first()
    if not session or session.status != "completed" or not session.overall_score:
        raise HTTPException(status_code=404, detail="Session not found or not completed.")
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(A4))
    w, h = landscape(A4)
    
    # Colors
    gold = (0.831, 0.686, 0.216)  # #D4AF37
    teal = (0, 0.5, 0.4)          # Primary brand
    dark = (0.1, 0.1, 0.1)
    
    # Watermark (rotated "VERIFIED" text)
    c.saveState()
    c.setFont("Helvetica-Bold", 120)
    c.setFillColorRGB(*gold, alpha=0.08)
    c.translate(w/2, h/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "VERIFIED")
    c.restoreState()
    
    # Outer gold border (thick)
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(4)
    c.rect(30, 30, w - 60, h - 60, stroke=1, fill=0)
    
    # Inner teal border (thinner)
    c.setStrokeColorRGB(*teal)
    c.setLineWidth(2)
    c.rect(40, 40, w - 80, h - 80, stroke=1, fill=0)
    
    # Decorative corner accents (4 corners)
    corner_size = 30
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(1.5)
    # Top-left
    c.line(40, h - 70, 40 + corner_size, h - 70)
    c.line(40, h - 70, 40, h - 70 - corner_size)
    # Top-right
    c.line(w - 40, h - 70, w - 40 - corner_size, h - 70)
    c.line(w - 40, h - 70, w - 40, h - 70 - corner_size)
    # Bottom-left
    c.line(40, 70, 40 + corner_size, 70)
    c.line(40, 70, 40, 70 + corner_size)
    # Bottom-right
    c.line(w - 40, 70, w - 40 - corner_size, 70)
    c.line(w - 40, 70, w - 40, 70 + corner_size)
    
    # Logo (geometric shield with circuit)
    logo_x, logo_y = 80, h - 90
    c.setFillColorRGB(*teal)
    c.setStrokeColorRGB(*teal)
    c.setLineWidth(1)
    # Shield outline
    shield_path = c.beginPath()
    shield_path.moveTo(logo_x, logo_y)
    shield_path.lineTo(logo_x + 40, logo_y)
    shield_path.lineTo(logo_x + 35, logo_y - 50)
    shield_path.lineTo(logo_x + 20, logo_y - 60)
    shield_path.lineTo(logo_x + 5, logo_y - 50)
    shield_path.close()
    c.drawPath(shield_path, stroke=0, fill=1)
    # Circuit lines inside shield
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1.5)
    c.line(logo_x + 10, logo_y - 15, logo_x + 30, logo_y - 15)
    c.line(logo_x + 20, logo_y - 15, logo_x + 20, logo_y - 35)
    c.line(logo_x + 15, logo_y - 25, logo_x + 25, logo_y - 25)
    # Circuit nodes
    c.setFillColorRGB(*gold)
    c.circle(logo_x + 10, logo_y - 15, 2, stroke=0, fill=1)
    c.circle(logo_x + 30, logo_y - 15, 2, stroke=0, fill=1)
    c.circle(logo_x + 20, logo_y - 35, 2, stroke=0, fill=1)
    
    # Title
    c.setFont("Helvetica-Bold", 48)
    c.setFillColorRGB(*teal)
    c.drawCentredString(w/2, h - 120, "CyberVerse AI")
    
    # Subtitle
    c.setFont("Helvetica", 28)
    c.setFillColorRGB(*dark)
    c.drawCentredString(w/2, h - 180, "Certificate of Completion")
    
    # Horizontal divider
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(1)
    c.line(w/2 - 150, h - 210, w/2 + 150, h - 210)
    
    # Certification text
    c.setFont("Helvetica", 18)
    name = user.full_name or user.email.split("@")[0]
    c.drawCentredString(w/2, h - 260, f"This certifies that {name}")
    c.drawCentredString(w/2, h - 300, f"has successfully completed the {session.role} Mock Interview")
    
    # Score (gold accent)
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(*gold)
    c.drawCentredString(w/2, h - 380, f"Score: {session.overall_score}/100")
    
    # Date
    from datetime import datetime as _dt
    date_str = session.created_at.strftime("%B %d, %Y") if hasattr(session, 'created_at') else _dt.utcnow().strftime("%B %d, %Y")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(*dark)
    c.drawCentredString(w/2, h - 430, f"Issued on {date_str}")
    
    # Signature block
    c.setStrokeColorRGB(*dark)
    c.setLineWidth(0.5)
    c.line(w/2 - 100, 140, w/2 + 100, 140)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w/2, 125, "Gaurav Malhotra")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w/2, 110, "Founder, CyberVerse AI")
    
    # Verification footer
    import hashlib as _h
    verify_id = _h.sha256(f"{session.id}-{session.user_id}-{session.created_at}".encode()).hexdigest()[:12]
    verify_url = f"grcwithgaurav.com/verify/{verify_id}"
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*teal)
    c.drawCentredString(w/2, 60, f"Verify authenticity: {verify_url}")
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(w/2, 45, "This certificate was earned through demonstrated competency in AI-simulated interviews")
    
    c.showPage()
    c.save()
    packet.seek(0)
    return StreamingResponse(packet, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=cyberverse_{session.id}_certificate.pdf"})
