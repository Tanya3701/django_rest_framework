from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson
from lessons.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsAuthorOrReadOnly, ModeratorsPermission


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.author_course = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~ModeratorsPermission,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (ModeratorsPermission | IsAuthorOrReadOnly,)
        elif self.action == "destroy":
            self.permission_classes = (~ModeratorsPermission | IsAuthorOrReadOnly,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        ~ModeratorsPermission,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.author_lesson = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ModeratorsPermission | IsAuthorOrReadOnly,
    )


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ModeratorsPermission | IsAuthorOrReadOnly,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnly | ~ModeratorsPermission,
    )
