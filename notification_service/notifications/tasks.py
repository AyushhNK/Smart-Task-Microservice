from celery import shared_task
from .models import Notification

@shared_task
def create_notification(user_id, message):
    Notification.objects.create(
        user_id=user_id,
        message=message
    )