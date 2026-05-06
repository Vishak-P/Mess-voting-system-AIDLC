"""
Notification utilities.
Twilio SMS integration (mock/placeholder for production).
"""
import os
import logging

logger = logging.getLogger(__name__)


def send_sms(to_number: str, message: str) -> bool:
    """
    Send SMS via Twilio.
    Returns True on success, False on failure.
    In development, logs the message instead of sending.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
    from_number = os.getenv("TWILIO_PHONE_NUMBER", "")

    if not all([account_sid, auth_token, from_number]):
        # Mock: just log the message
        logger.info(f"[SMS MOCK] To: {to_number} | Message: {message}")
        return True

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_number, to=to_number)
        logger.info(f"SMS sent to {to_number}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False


def notify_voting_open(menu_date: str, meal_type: str, deadline: str):
    """Placeholder: notify students that voting is open."""
    message = (
        f"Voting is now open for {meal_type} on {menu_date}. "
        f"Cast your vote before {deadline}!"
    )
    logger.info(f"[NOTIFICATION] {message}")
    return message


def notify_voting_closed(menu_date: str, meal_type: str):
    """Placeholder: notify students that voting has closed."""
    message = f"Voting for {meal_type} on {menu_date} has closed. Check the results!"
    logger.info(f"[NOTIFICATION] {message}")
    return message
