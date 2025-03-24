from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Lesson, Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(verbose_name='Мобильный телефон', max_length=30, blank=True)
    avatar = models.ImageField(verbose_name='Фотография', upload_to='users/', blank=True, null=True)
    city = models.CharField(max_length=255, unique=True, verbose_name='Город', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['email', ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Payment(models.Model):
    PAYMENT_TYPE = {
        'account': 'Счет',
        'cash': 'Наличные'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', auto_now_add=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, verbose_name='Тип оплаты', max_length=10)
    lesson = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE, related_name='payments')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date', ]

    def __str__(self):
        return f'Платеж {self.pk} на сумму {self.amount} рублей от {self.user}'
