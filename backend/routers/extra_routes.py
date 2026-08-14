from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date

import models
from auth import get_current_user
from database import get_db

router = APIRouter(tags=["extra"])

BANK = [
 {"question": "Which Windows Event ID indicates a FAILED logon attempt?", "options": ["4624", "4625", "4688", "4769"], "answer": 1, "explanation": "4625 = failed logon; 4624 = success.", "xp": 10},
 {"question": "An email urges urgent invoice payment; the header shows a look-alike domain. First action?", "options": ["Pay the invoice", "Report and quarantine the email", "Delete and ignore", "Reply to the sender"], "answer": 1, "explanation": "Treat as phishing: report and contain.", "xp": 10},
 {"question": "DNS tunneling exfiltrates data by abusing which protocol?", "options": ["HTTP", "DNS", "SMTP", "NTP"], "answer": 1, "explanation": "Data hidden in DNS queries/responses.", "xp": 10},
 {"question": "In the cyber kill chain, which stage follows Delivery?", "options": ["Reconnaissance", "Exploitation", "Installation", "Actions on Objectives"], "answer": 1, "explanation": "Recon > Weaponization > Delivery > Exploitation.", "xp": 10},
 {"question": "Which Splunk command counts events per host?", "options": ["stats count by host", "table host", "fields - host", "rename host"], "answer": 0, "explanation": "stats count by host aggregates per host.", "xp": 10},
 {"question": "A CVSS score of 9.0-10.0 is rated as?", "options": ["Low", "Medium", "High", "Critical"], "answer": 3, "explanation": "9.0-10.0 = Critical.", "xp": 10},
 {"question": "A Golden Ticket attack forges a TGT using which account hash?", "options": ["Administrator", "KRBTGT", "Guest", "LocalSystem"], "answer": 1, "explanation": "KRBTGT signs Kerberos TGTs.", "xp": 10},
]

def today_q():
    return BANK[date.today().toordinal() % len(BANK)]

class CtfSubmit(BaseModel):
    answer: int

@router.get("/api/ctf/today")
def ctf_today(user: models.User = Depends(get_current_user)):
    q = today_q()
    return {"question": q["question"], "options": q["options"], "explanation": q["explanation"], "xp": q["xp"]}

@router.post("/api/ctf/submit")
def ctf_submit(p: CtfSubmit, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = today_q()
    correct = p.answer == q["answer"]
    xp = 0
    day = date.today().isoformat()
    if correct:
        existing = db.query(models.CtfSolve).filter(models.CtfSolve.user_id == user.id, models.CtfSolve.solve_date == day).first()
        if not existing:
            db.add(models.CtfSolve(user_id=user.id, solve_date=day, xp=q["xp"]))
            user.xp = (user.xp or 0) + q["xp"]
            xp = q["xp"]
            db.commit()
    return {"correct": correct, "xp": xp}

@router.get("/api/leaderboard")
def leaderboard(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.User).order_by(models.User.xp.desc()).limit(20).all()
    users = []
    for u in rows:
        users.append({"name": u.full_name or u.email.split("@")[0], "xp": u.xp or 0,
                      "is_pro": bool(getattr(u, "is_premium", False) or getattr(u, "is_pro", False))})
    return {"users": users}
