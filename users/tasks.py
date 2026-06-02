import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def activity_check():
    user_verification = User.objects.filter(is_active=True)
    for user in user_verification:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            logger.info(
                f"Пользователь {user.email} деактивирован, по причине бездействия"
            )
