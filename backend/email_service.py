"""
Minimal email sender. Works with any SMTP provider (Gmail app password,
SendGrid SMTP relay, Postmark, AWS SES SMTP, etc.) - just set SMTP_* in .env.

If SMTP_HOST is unset, emails are logged to the console instead of sent.
That's fine for local dev; it is NOT fine for production - the app will
still "work" but nobody will receive password reset emails.
"""
import logging
import smtplib
from email.message import EmailMessage

from config import settings

logger = logging.getLogger("cyberverse.email")


def send_email(to: str, subject: str, body: str) -> None:
    if not settings.smtp_host:
        logger.warning(
            "SMTP not configured - logging email instead of sending.\n"
            "TO: %s\nSUBJECT: %s\nBODY:\n%s",
            to, subject, body,
        )
        return

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
    reset_link = f"{settings.app_base_url}/?reset_token={reset_token}"
    body = (
        f"We received a request to reset your CyberVerse AI password.\n\n"
        f"Reset it here (expires in {settings.reset_token_expire_minutes} minutes):\n"
        f"{reset_link}\n\n"
        f"If you didn't request this, you can safely ignore this email."
    )
    send_email(to, "Reset your CyberVerse AI password", body)
