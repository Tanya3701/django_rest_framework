from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    lesson = models.ForeignKey(
        "lessons.lesson", on_delete=models.CASCADE, null=True, blank=True
    )
    course = models.ForeignKey(
        "lessons.course", on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.PositiveIntegerField(default=0)
    payment_form = models.CharField(
        choices=[
            ("cash", "Наличные"),
            ("non-cash", "Безналичные"),
        ],
        null=True,
        blank=True,
    )
    link = models.URLField(max_length=1000, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.amount
