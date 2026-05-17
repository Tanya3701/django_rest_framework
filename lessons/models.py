from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    preview = models.ImageField(
        upload_to="lessons/images/", null=True, blank=True
    )
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(
        upload_to="lessons/images/", null=True, blank=True
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
