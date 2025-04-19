from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(verbose_name="Название курса", max_length=255)
    avatar = models.ImageField(
        verbose_name="Превью", upload_to="lms/course", blank=True, null=True
    )
    city = models.CharField(max_length=255, verbose_name="Город", blank=True, null=True)
    owner = models.ForeignKey(
        User,
        related_name="courses",
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.PROTECT, related_name="lessons"
    )
    title = models.CharField(verbose_name="Название урока", max_length=255)
    description = models.TextField(verbose_name="Описание")
    avatar = models.ImageField(
        verbose_name="Превью", upload_to="lms/lesson/img", blank=True, null=True
    )
    video = models.FileField(upload_to="lms/lesson/video", blank=True, null=True)
    owner = models.ForeignKey(
        User,
        related_name="lessons",
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = [
            "title",
            "course",
        ]

    def __str__(self):
        return self.title


class Payment(models.Model):
    PAYMENT_TYPE = {"account": "Счет", "cash": "Наличные"}

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    amount = models.IntegerField(verbose_name="Сумма оплаты")
    payment_date = models.DateTimeField(verbose_name="Дата оплаты", auto_now_add=True)
    payment_type = models.CharField(
        choices=PAYMENT_TYPE, verbose_name="Тип оплаты", max_length=10
    )
    lesson = models.ForeignKey(
        Lesson, blank=True, null=True, on_delete=models.CASCADE, related_name="payments"
    )
    course = models.ForeignKey(
        Course, blank=True, null=True, on_delete=models.CASCADE, related_name="payments"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = [
            "-payment_date",
        ]

    def __str__(self):
        return f"Платеж {self.pk} на сумму {self.amount} рублей от {self.user}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="sub",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="sub",
        blank=True,
        null=True,
    )


class CoursePayment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="course_payments",
        verbose_name="Пользователь",
        blank=True,
        null=True,
        help_text="Укажите пользователя",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_payments",
        verbose_name="Курс",
        blank=True,
        null=True,
        help_text="Укажите курс",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Оплата курса"
        verbose_name_plural = "Оплаты курсов"

    def __str__(self):
        return f"{self.user} - {self.course} - {self.amount}"
