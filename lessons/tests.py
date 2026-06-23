from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Course, Lesson, Subscription
from users.models import User


class LessonsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.test")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test", description="test, test", course=self.course, owner=self.user
        )
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lessons:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Test Course")

    def test_course_create(self):
        url = reverse("lessons:course-list")
        data = {"title": "Test Course 2", "description": "Test Course 2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_list(self):
        url = reverse("lessons:course-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "description": self.course.description,
                    "lessons_in_course_count": 1,
                    "lessons_in_lesson": ["test"],
                    "owner": self.user.pk,
                    "subscription": True,
                }
            ],
        }
        self.assertEqual(data, result)

    # def test_course_update(self):
    #     url = reverse("lessons:course-detail", args=(self.course.pk,))
    #     data = {"description": "Test Course 2"}
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("description"), "Test Course 2")

    def test_course_delete(self):
        url = reverse("lessons:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_lesson_retrieve(self):
        url = reverse("lessons:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test")

    def test_lesson_create(self):
        url = reverse("lessons:lesson_create")
        data = {"title": "test 2", "description": "test 2", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        url = reverse("lessons:lesson_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_lesson_update(self):
        url = reverse("lessons:lesson_update", args=(self.lesson.pk,))
        data = {"description": "test 2"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), "test 2")

    def test_lesson_delete(self):
        url = reverse("lessons:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription(self):
        url = reverse("lessons:subscription")
        data = {"course_id": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
