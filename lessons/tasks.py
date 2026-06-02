from datetime import timedelta, datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lessons.models import Course, Subscription


@shared_task
def send_email_about_updates(course_id):
    course = Course.objects.get(id=course_id)
    if timezone.now() - course.updated_at > timedelta(hours=4):
        subscriptions = Subscription.objects.filter(course_id=course_id).select_related(
            "user"
        )
        subscriptions_users = [subscription.user.email for subscription in subscriptions]
        send_mail(
            subject="Обновление курса",
            message=f"Курс {course.title} обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=subscriptions_users,
        )
        print("Письмо отправлено")
    else:
        print("Письмо не отправлено")
