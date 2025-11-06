import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from .models import ContactMessage

def sync_send_contact_email(message_id: int):
    msg_obj = ContactMessage.objects.get(pk=message_id)
    sg_api_key = settings.SENDGRID_API_KEY
    if not sg_api_key:
        raise RuntimeError("SENDGRID_API_KEY not set")

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.CONTACT_RECIPIENT]

    subject = msg_obj.subject or f'New contact from {msg_obj.name}'
    html_content = f"""
        <p><strong>Name:</strong> {msg_obj.name}</p>
        <p><strong>Email:</strong> {msg_obj.email}</p>
        <p><strong>Message:</strong><br/>{msg_obj.message}</p>
        <p><small>ID: {msg_obj.id}</small></p>
    """
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(sg_api_key)
        resp = sg.send(message)
        # optional: check resp.status_code
        msg_obj.sent = True
        msg_obj.save()
        return resp
    except Exception as e:
        msg_obj.error = str(e)
        msg_obj.save()
        raise
