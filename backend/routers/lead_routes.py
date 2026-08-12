from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

import models
from database import get_db
from email_service import send_lead_magnet_email
from rate_limit import limiter

router = APIRouter(prefix="/api/leads", tags=["leads"])

class LeadIn(BaseModel):
    email: EmailStr

@router.post("")
@limiter.limit("5/hour")
def add_lead(request: Request, payload: LeadIn, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if not db.query(models.Lead).filter(models.Lead.email == email).first():
        db.add(models.Lead(email=email))
        db.commit()
    send_lead_magnet_email(email, "https://app.grcwithgaurav.com/downloads/soc-interview-questions.pdf")
    return {"message": "Sent! Check your inbox (and spam folder)."}
