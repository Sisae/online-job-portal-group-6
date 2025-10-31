from typing import Iterable, Optional, Dict, Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def get_default_from_email() -> str:
    return getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', '') or 'no-reply@example.com'


def send_plain_email(subject: str, message: str, recipients: Iterable[str], from_email: Optional[str] = None) -> int:
    recipient_list = [email for email in recipients if email]
    if not recipient_list:
        return 0
    return send_mail(subject, message, from_email or get_default_from_email(), recipient_list, fail_silently=False)


def send_templated_email(
    subject: str,
    template_name: str,
    context: Optional[Dict[str, Any]],
    recipients: Iterable[str],
    from_email: Optional[str] = None,
) -> int:
    message = render_to_string(template_name, context or {})
    return send_plain_email(subject, message, recipients, from_email)


def send_sms_stub(phone_numbers: Iterable[str], message: str) -> int:
    """
    Placeholder for SMS integration (e.g., Twilio). Returns count that would be sent.
    """
    numbers = [p for p in phone_numbers if p]
    # Integrate provider here. For now, no-op.
    return len(numbers)


