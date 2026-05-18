from django.contrib.auth.models import AbstractUser
from django.db import models

from lessons.models import Lesson, Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_form = models.CharField(choices=[("cash", "Наличные"), ("non-cash", "Безналичные")])

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.user.email