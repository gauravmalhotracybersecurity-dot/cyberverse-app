"""
Email delivery, with two backends:

1. Resend (HTTPS API) - works everywhere, including hosts that block
   outbound SMTP ports (Render, Railway, Heroku free tiers, etc). Used
   automatically when RESEND_API_KEY is set. This is the recommended path.
2. SMTP - only works on hosts that allow outbound SMTP connections (a real
   VPS typically does; most PaaS free tiers don't). Used when RESEND_API_KEY
   is unset but SMTP_HOST is set.

If neither is configured, emails are logged instead of sent - fine for local
dev, not for production.

Delivery failures are always caught and logged, never raised - a broken
email provider should never turn into a 500 for the person requesting a
password reset. The generic "if that email is registered..." response in
auth_routes.py still gets returned either way, so this also avoids leaking
whether the send actually succeeded (which would itself leak whether the
account exists).
"""
import logging
import smtplib
from email.message import EmailMessage

import httpx

from config import settings

logger = logging.getLogger("cyberverse.email")

RESEND_API_URL = "https://api.resend.com/emails"


def send_email(to: str, subject: str, body: str) -> None:
    try:
        if settings.resend_api_key:
            _send_via_resend(to, subject, body)
        elif settings.smtp_host:
            _send_via_smtp(to, subject, body)
        else:
            logger.warning(
                "No email provider configured - logging email instead of sending.\n"
                "TO: %s\nSUBJECT: %s\nBODY:\n%s",
                to, subject, body,
            )
    except Exception:
        logger.exception("Failed to send email to %s (subject: %s)", to, subject)


def _send_via_resend(to: str, subject: str, body: str) -> None:
    resp = httpx.post(
        RESEND_API_URL,
        headers={"Authorization": f"Bearer {settings.resend_api_key}"},
        json={
            "from": settings.resend_from_email,
            "to": [to],
            "subject": subject,
            "text": body,
        },
        timeout=15,
    )
    resp.raise_for_status()


def _send_via_smtp(to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = settings.smtp_from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_user:
            server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)


def send_password_reset_email(to: str, reset_token: str) -> None:
    reset_link = f"{settings.app_base_url}/app.html?reset_token={reset_token}"
    body = (
        f"We received a request to reset your CyberVerse AI password.\n\n"
        f"Reset it here (expires in {settings.reset_token_expire_minutes} minutes):\n"
        f"{reset_link}\n\n"
        f"If you didn't request this, you can safely ignore this email."
    )
    send_email(to, "Reset your CyberVerse AI password", body)


def send_welcome_email(to: str, full_name: str) -> None:
    first_name = full_name.split()[0] if full_name else "there"
    subject = f"Welcome to CyberVerse AI, {first_name}!"
    body = (
        f"Hey {first_name},\n\n"
        "Welcome to CyberVerse AI! I'm Gaurav, the founder.\n\n"
        "Here is your 3-step quick start plan:\n\n"
        "1. Upload your resume: The AI will review it like a recruiter.\n"
        "2. Check Daily Ops: Get a personalized lesson and quiz every morning.\n"
        "3. Start a mock interview: Try a 5-question interview.\n\n"
        "Best,\nGaurav\nFounder, CyberVerse AI"
    )
    send_email(to, subject, body)


def send_interview_nudge_email(to: str, full_name: str, role: str) -> None:
    first_name = full_name.split()[0] if full_name else "there"
    subject = f"Your {role} interviewer is waiting for you 🎙️"
    body = (
        f"Hey {first_name},\n\n"
        f"You started a {role} mock interview on CyberVerse AI a couple of hours ago but didn't finish it.\n\n"
        f"The best way to get hired is to practice under pressure. Jump back in and finish your 6 questions now. It only takes 10 minutes, and you will get a score out of 100 at the end.\n\n"
        f"Log in and finish it here: {settings.app_base_url}/app.html\n\n"
        f"You've got this.\n"
        f"- The CyberVerse AI Interviewer"
    )
    send_email(to, subject, body)


def send_verification_email(to: str, link: str) -> None:
    subject = "Verify your CyberVerse AI email"
    body = (
        "Welcome to CyberVerse AI!\n\n"
        "Click the link below to verify your email address and activate your account:\n"
        f"{link}\n\n"
        "If you didn't create this account, you can safely ignore this email."
    )
    send_email(to, subject, body)


def send_day3_nurture_email(to: str, full_name: str, weak_topics: list, unfinished_interviews: int) -> None:
    first_name = full_name.split()[0] if full_name else "there"
    subject = f"{first_name}, your cybersecurity career is waiting on you"
    topics_str = ", ".join(weak_topics[:3]) if weak_topics else "SQL Injection, Firewalls, SIEM tools"
    body = (
        f"Hey {first_name},\n\n"
        f"It's been 3 days since you joined CyberVerse AI. Most candidates who get hired do their first mock interview within the first week.\n\n"
        f"Based on your profile, here are your top weak spots to focus on:\n"
        f"→ {topics_str}\n\n"
    )
    if unfinished_interviews > 0:
        body += f"You have {unfinished_interviews} interview(s) you started but never finished. Finishing just one gives you a score out of 100 and tells you exactly what to study next.\n\n"
    body += (
        f"Log in and pick up where you left off: {settings.app_base_url}/app.html\n\n"
        f"The longer you wait, the more ground you lose to other candidates.\n\n"
        f"- The CyberVerse AI team"
    )
    send_email(to, subject, body)


def send_day7_nurture_email(to: str, full_name: str, resume_score: int, xp: int) -> None:
    first_name = full_name.split()[0] if full_name else "there"
    subject = f"7 days, {first_name}. Still no interview practice?"
    body = (
        f"Hey {first_name},\n\n"
        f"It's been a week. Most cybersecurity professionals who land interviews practice at least once a week. You haven't logged in.\n\n"
    )
    if resume_score:
        body += f"Your resume scored {resume_score}/100. That's a start, but a resume alone doesn't get you hired — defending your answers in an interview does.\n\n"
    body += (
        f"You've earned {xp} XP so far. Every day you don't practice, other candidates are pulling ahead.\n\n"
        f"Here's what to do right now (takes 10 minutes):\n"
        f"1. Log in: {settings.app_base_url}/app.html\n"
        f"2. Start a mock interview (any role)\n"
        f"3. Get your score out of 100\n\n"
        f"Your future self will thank you.\n\n"
        f"- The CyberVerse AI team"
    )
    send_email(to, subject, body)
