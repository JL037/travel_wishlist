import httpx
import logging
from fastapi import BackgroundTasks
from app.core.config import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"

async def send_password_reset_email(background_tasks: BackgroundTasks, to_email: str, reset_token: str):
    reset_url = f"https://travelwishlist.app/reset-password?token={reset_token}"

    html = f"""
    <p>Hello,</p>
    <p>You requested to reset your password.</p>
    <p>Click below to reset it:</p>
    <a href="{reset_url}">{reset_url}</a>
    <p>If you didn't request this, ignore it.</p>
    """

    background_tasks.add_task(_send_email, to_email, "Reset Your Password", html)

async def _send_email(to: str, subject: str, html: str):
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "from": "Travel Wishlist <noreply@travelwishlist.app>",
        "to": [to],
        "subject": subject,
        "html": html,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(RESEND_API_URL, headers=headers, json=data)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Email failed to send: {exc.response.status_code} - {exc.response.text}")
        except Exception:
            logger.exception("Unexpected error sending email")
