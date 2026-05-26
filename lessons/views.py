from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson, Subscription
from lessons.pagination import CustomPageNumberPagination
from lessons.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsAuthorOrReadOnly, ModeratorsPermission


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.author_course = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                ~ModeratorsPermission,
                IsAuthenticated,
            )
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
    pagination_class = CustomPageNumberPagination


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


class SubscriptionAPIView(CreateAPIView):
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data["course_id"]
        course_item = get_object_or_404(Course, pk=course_id)
        subscription_item = Subscription.objects.filter(user=user, course=course_item)
        if subscription_item.exists():
            subscription_item.delete()
            message = "Подписка удалена"
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            return Response({"message": message}, status=status.HTTP_201_CREATED)
