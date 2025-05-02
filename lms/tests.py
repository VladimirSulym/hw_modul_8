from django.urls.base import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@test.ru")
        self.course = Course.objects.create(title="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание тестового урока",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["results"],
            [
                {
                    "id": 4,
                    "title": "Тестовый урок",
                    "description": "Описание тестового урока",
                    "avatar": None,
                    "video": None,
                    "course": 3,
                    "owner": 3,
                }
            ],
        )

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "Новый тестовый урок",
            "description": "Описание нового урока",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "Обновленное название урока",
            "description": "Описание нового урока",
            "course": self.course.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Обновленное название урока")

    def test_lesson_delete(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.pk).exists())


class SubTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@test.ru")
        self.course = Course.objects.create(title="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание тестового урока",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_sub(self):
        url = reverse("lms:subscription")
        response = self.client.post(url, {"course": self.course.pk})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["message"], "подписка добавлена")

        response = self.client.post(url, {"course": self.course.pk})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["message"], "подписка удалена")
