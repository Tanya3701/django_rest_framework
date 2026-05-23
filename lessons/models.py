from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="lessons/images/", null=True, blank=True, verbose_name="Изображение"
    )
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Автор курса",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок урока")
    description = models.TextField(verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="lessons/images/", null=True, blank=True, verbose_name="Изображение"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    link = models.URLField(verbose_name="Ссылка", null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор урока",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

