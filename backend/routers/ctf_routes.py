from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
import base64, codecs

import models
from auth import get_current_user
from database import get_db
from rate_limit import limiter

router = APIRouter(prefix="/api/ctf", tags=["ctf"])

def _bank():
    f1, f2, f3 = "CV{base64_wizard}", "CV{hex_hero}", "CV{caesar_slayer}"
    return [
      {"id":"b64","title":"Decode the blob","prompt":"Decode this Base64:\n"+base64.b64encode(f1.encode()).decode(),"answers":[f1],"hint":"any base64 decoder (or `base64 -d`)","explain":"Base64 maps binary to 64 ASCII characters; decoding reveals the flag."},
      {"id":"hex","title":"Hex whisperer","prompt":"Decode this hex:\n"+f2.encode().hex(),"answers":[f2],"hint":"every two hex chars = one byte","explain":"Hex is base-16; convert each byte pair back to ASCII."},
      {"id":"rot13","title":"Caesar's lazy cousin","prompt":"Decode this ROT13:\n"+codecs.encode(f3,"rot13"),"answers":[f3],"hint":"rotate the alphabet by 13","explain":"ROT13 shifts letters by 13; applying it twice returns the original."},
      {"id":"xss","title":"Spot the XSS","prompt":"One line hides an XSS payload. Which attribute fires it?\n\n1. <div class=\"note\">Hello</div>\n2. <img src=x onerror=alert(document.cookie)>\n3. <a href=\"/home\">Home</a>\n4. <p title=\"info\">Text</p>","answers":["onerror","2","line 2"],"hint":"which event fires when the image fails to load?","explain":"onerror runs JavaScript when the image fails to load - a classic XSS vector."},
      {"id":"phish","title":"Phish or dish?","prompt":"Which URL is malicious?\n\na) https://login.microsoft.com\nb) https://micros0ft-login.com\nc) https://portal.office.com","answers":["b","micros0ft-login.com"],"hint":"look for the zero","explain":"Lookalike domains (micros0ft with a zero) are a classic phishing tell."},
      {"id":"port-rdp","title":"Port check","prompt":"Default port for RDP?","answers":["3389"],"hint":"3-3-8-9","explain":"RDP defaults to TCP 3389 - a favorite brute-force target."},
      {"id":"port-ssh","title":"Port check II","prompt":"Default port for SSH?","answers":["22"],"hint":"twenty-two","explain":"SSH defaults to TCP 22."},
      {"id":"eventid","title":"Event ID hunt","prompt":"Windows Event ID for a FAILED logon?  4624 / 4625 / 4688","answers":["4625"],"hint":"25 = fail","explain":"4624 = success, 4625 = failure, 4688 = process creation."},
      {"id":"sqli","title":"Injection instinct","prompt":"Which input is a classic SQL injection attempt?\n\na) admin@example.com\nb) ' OR 1=1 --\nc) P@ssw0rd!","answers":["b","' or 1=1 --","or 1=1"],"hint":"quote + tautology","explain":"' OR 1=1 -- makes the WHERE clause always true, bypassing auth."},
      {"id":"krbtgt","title":"Kerberos crown","prompt":"A Golden Ticket attack forges a TGT signed by which account?","answers":["krbtgt"],"hint":"the KDC's own key","explain":"Golden Tickets are forged with the KRBTGT account hash."},
      {"id":"nosniff","title":"Header hero","prompt":"Which response header stops MIME-sniffing XSS?","answers":["x-content-type-options","nosniff","x-content-type-options: nosniff"],"hint":"no sniffing","explain":"X-Content-Type-Options: nosniff stops browsers from MIME-sniffing responses into executable types."},
      {"id":"tls","title":"TLS trust","prompt":"In a TLS handshake, which message proves the server's identity?","answers":["certificate","server certificate","the certificate"],"hint":"it carries the public key","explain":"The server certificate, chained to a trusted CA, proves identity."},
    ]

def _today():
    bank = _bank()
    return bank[int(date.today().strftime("%Y%m%d")) % len(bank)]

class CTFSubmit(BaseModel):
    answer: str
    elapsed: int = 999

@router.get("/today")
def ctf_today(user: models.User = Depends(get_current_user)):
    ch = _today()
    return {"id": ch["id"], "title": ch["title"], "prompt": ch["prompt"], "hint": ch["hint"],
            "solved_today": str(user.ctf_last_solved_date) == str(date.today()),
            "solves": user.ctf_solves or 0}

@router.post("/submit")
@limiter.limit("30/hour")
def ctf_submit(request: Request, payload: CTFSubmit, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    ch = _today()
    norm = lambda t: t.strip().lower()
    if norm(payload.answer) not in [norm(a) for a in ch["answers"]]:
        return {"correct": False, "hint": ch["hint"]}
    already = str(user.ctf_last_solved_date) == str(date.today())
    xp = 0
    if not already:
        user.ctf_solves = (user.ctf_solves or 0) + 1
        user.ctf_last_solved_date = date.today()
        xp = 10
        if payload.elapsed <= 60:
            xp += 5
        user.xp += xp
        db.commit()
    return {"correct": True, "explain": ch["explain"], "xp": xp, "already": already}
