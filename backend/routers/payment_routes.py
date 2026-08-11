from datetime import datetime as _dt
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import hmac, hashlib, json, logging
from config import settings
from database import get_db
import models

logger = logging.getLogger("cyberverse.payments")
router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


def _verify(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        settings.razorpay_webhook_secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/razorpay")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    if not signature or not _verify(body, signature):
        logger.warning("Razorpay webhook rejected: bad signature.")
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        payload = json.loads(body)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad JSON")

    event = payload.get("event", "")
    if event not in ("payment_link.paid", "payment.captured"):
        return {"status": "ignored", "event": event}

    # Robust extraction of customer email across Razorpay payload shapes
    pl = payload.get("payload", {}).get("payment_link", {}) or {}
    entity = pl.get("entity", pl) if isinstance(pl, dict) else {}
    customer = entity.get("customer", {}) if isinstance(entity, dict) else {}
    email = (customer.get("email") or "").strip().lower()

    if not email:
        pay = payload.get("payload", {}).get("payment", {}) or {}
        pay_entity = pay.get("entity", pay) if isinstance(pay, dict) else {}
        email = (pay_entity.get("email") or "").strip().lower()

    if not email:
        logger.warning("Webhook received but no customer email found.")
        return {"status": "no_email"}

    # Extract amount in paise (99900 = 999 INR)
    amount = entity.get("amount", 0) if isinstance(entity, dict) else 0
    
    user = db.query(models.User).filter(func.lower(models.User.email) == email).first()
    if user:
        upgraded = False
        if amount == 4900: # Streak Rescue
            user.last_active_date = _dt.utcnow().date()
            upgraded = True
            logger.info("User %s rescued streak for 49.", email)
        elif amount == 99900: # Premium Tier
            if not user.is_premium:
                user.is_pro = True
                user.is_premium = True
                upgraded = True
                logger.info("User %s upgraded to PREMIUM.", email)
        elif amount == 49900: # Pro Tier
            if not user.is_pro:
                user.is_pro = True
                upgraded = True
                logger.info("User %s upgraded to Pro.", email)
        
        if upgraded:
            db.commit()
            return {"status": "upgraded", "email": email, "tier": "Premium" if amount == 99900 else "Pro"}
            
    return {"status": "already_pro_or_unknown", "email": email}