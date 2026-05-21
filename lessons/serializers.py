from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lessons.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_in_course_count = SerializerMethodField()
    lessons_in_lesson = SerializerMethodField()

    @staticmethod
    def get_lessons_in_course_count(obj):
        return Lesson.objects.filter(course=obj).count()

    @staticmethod
    def get_lessons_in_lesson(obj):
        return [lesson.title for lesson in Lesson.objects.filter(course=obj)]

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_in_course_count",
            "lessons_in_lesson",
            "author_course",
        )
