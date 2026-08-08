from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from claude_client import call_claude_json, ClaudeClientError
from config import settings
from database import get_db
from prompts import resume_review_system_prompt
from rate_limit import limiter
from resume_parsing import extract_resume_text
from weak_topics import merge_weak_topics

router = APIRouter(prefix="/api/resume", tags=["resume"])


async def _run_review(resume_text: str, target_role: str, user: models.User, db: Session):
    try:
        review = await call_claude_json(
            system=resume_review_system_prompt(target_role),
            messages=[{"role": "user", "content": f"Resume text:\n\n{resume_text}"}],
            max_tokens=2000,
        )
    except ClaudeClientError as e:
        raise HTTPException(status_code=502, detail=str(e))

    record = models.ResumeReview(user_id=user.id, resume_text=resume_text, review=review)
    db.add(record)
    user.xp += 15
    merge_weak_topics(user, review.get("missing_skills_for_target_role"))
    db.commit()
    db.refresh(record)

    return schemas.ResumeReviewResponse(
        id=record.id, review=review, created_at=record.created_at.isoformat()
    )


@router.post("/review", response_model=schemas.ResumeReviewResponse)
@limiter.limit(settings.rate_limit_resume)
async def review_resume(
    request: Request,
    payload: schemas.ResumeReviewRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Review a resume submitted as pasted text."""
    return await _run_review(payload.resume_text, payload.target_role, user, db)


@router.post("/review-upload", response_model=schemas.ResumeReviewResponse)
@limiter.limit(settings.rate_limit_resume)
async def review_resume_upload(
    request: Request,
    file: UploadFile = File(...),
    target_role: str = Form("SOC Analyst"),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Review a resume submitted as a .pdf, .docx, or .txt file upload."""
    resume_text = await extract_resume_text(file)
    return await _run_review(resume_text, target_role, user, db)


@router.get("/history", response_model=list[schemas.ResumeReviewResponse])
def resume_history(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(models.ResumeReview)
        .filter(models.ResumeReview.user_id == user.id)
        .order_by(models.ResumeReview.created_at.desc())
        .all()
    )
    return [
        schemas.ResumeReviewResponse(id=r.id, review=r.review, created_at=r.created_at.isoformat())
        for r in records
    ]
