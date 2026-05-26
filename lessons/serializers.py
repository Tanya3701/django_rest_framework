from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lessons.models import Course, Lesson, Subscription
from lessons.validators import UrlValidator


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                fields=["course", "user"], queryset=Subscription.objects.all()
            )
        ]


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="link")]


class CourseSerializer(ModelSerializer):
    lessons_in_course_count = SerializerMethodField()
    lessons_in_lesson = SerializerMethodField()
    subscription = SerializerMethodField()
    sign_up = SubscriptionSerializer(source="subscription", many=True, read_only=True)

    @staticmethod
    def get_lessons_in_course_count(obj):
        return Lesson.objects.filter(course=obj).count()

    @staticmethod
    def get_lessons_in_lesson(obj):
        return [lesson.title for lesson in Lesson.objects.filter(course=obj)]

    def get_sign_up(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user).filter(course=obj).exists()

    def get_subscription(self, obj):
        return Subscription.objects.filter(course=obj).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_in_course_count",
            "lessons_in_lesson",
            "owner",
            "subscription",
            "sign_up",
        )
