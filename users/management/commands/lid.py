
from django.core.management.base import BaseCommand
import os

from dotenv import load_dotenv
import random

from lms.models import Course, Lesson
from users.models import User, Payment

load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        course_list = ['Python', 'SQL', 'C++', 'JS', 'SQLite', 'React']

        for index, value in enumerate(course_list):
            Course.objects.get_or_create(
                title=value,
                city='Москва' if index % 2 else 'Лондон'
            )
        self.stdout.write(self.style.SUCCESS(f"Курсы успешно созданы"))


        for course in Course.objects.all():
            for index in range(5):  # 5 уроков в каждом курсе
                Lesson.objects.get_or_create(
                    course=course,
                    title=f"Урок {index+1}",
                    description=f"Описание урока {index+1} по курсу {course}",
                )
        self.stdout.write(self.style.SUCCESS(f"Уроки успешно созданы"))

        user, created_user = User.objects.get_or_create(
            email="admin@admin.ru",
            first_name="Владимир",
            last_name="Сулым",
            phone="+7-985-123-45-67",
            city='Москва',
        )
        user.set_password(os.getenv("CSU_PASS"))
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Администратор успешно создан: {user.email}"))

        for index, value in enumerate(course_list):
            if index % 2:
                Payment.objects.create(
                    user=user,
                    amount=5000,
                    payment_type=random.choices(['account', 'cash'])[0],
                    course=Course.objects.get(title=value)
                )
                self.stdout.write(self.style.SUCCESS(f"Оплачен крус {value}"))
            else:
                for index in range(3):
                    lesson = random.choices(Lesson.objects.filter(course=Course.objects.get(title=value)))
                    Payment.objects.create(
                        user=user,
                        amount=1000,
                        payment_type=random.choices(['account', 'cash'])[0],
                        lesson=lesson[0]
                    )
                    self.stdout.write(self.style.SUCCESS(f"Оплачен урок {lesson[0]} в курсе {value}"))

