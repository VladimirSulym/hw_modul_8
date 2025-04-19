from datetime import timedelta
from django.utils import timezone

from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from users.models import User


@shared_task
def send_mail_user(message, course, lesson, users):
    for user in users:
        email = User.objects.get(id=user).email
        print(email)
        send_mail(
            f"Изменение в курсе на который вы подписаны",
            f"На курсе {course} {message} урок {lesson}",
            EMAIL_HOST_USER,
            [email],
        )

@shared_task
def check_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    for user in User.objects.all():
        print(f"Проверил {user}")
        if (user.last_login and user.last_login < month_ago) or (
            not user.last_login and user.date_joined < month_ago
        ):
            user.is_active = False
            user.save()
