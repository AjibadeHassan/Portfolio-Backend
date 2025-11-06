from celery import shared_task
from .emails import sync_send_contact_email
from .models import ContactMessage

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_contact_email(self, message_id):
    try:
        return sync_send_contact_email(message_id)
    except Exception as exc:
        # Optionally update DB
        try:
            msg = ContactMessage.objects.get(pk=message_id)
            msg.error = f'Retry error: {str(exc)}'
            msg.save()
        except ContactMessage.DoesNotExist:
            pass
        raise self.retry(exc=exc)
