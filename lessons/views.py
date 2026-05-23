from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson, Subscription
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
            self.permission_classes = (~ModeratorsPermission, IsAuthenticated,)
        elif self.action in ["update", "retrieve", "partial_update"]:
            self.permission_classes = (ModeratorsPermission | IsAuthorOrReadOnly,)
        elif self.action == "destroy":
            self.permission_classes = (~ModeratorsPermission | IsAuthorOrReadOnly,)
        elif self.action == "list":
            self.permission_classes = (IsAuthenticated | ModeratorsPermission,)
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
    permission_classes = (ModeratorsPermission | IsAuthenticated,)


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
        IsAuthorOrReadOnly, ~ModeratorsPermission,
    )

class SubscriptionAPIView(CreateAPIView):
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get("course_id")
        course_item = Course.objects.get(id=course_id)
        subscription_item = Subscription.objects.get(
            id=request.data.get(user=user, course=course_item)
        )
        if subscription_item.exists():
            subscription_item.delete()
            message = "Подписка удвлена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
