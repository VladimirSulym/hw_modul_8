from django.contrib.auth.models import AbstractUser
from django.db import models


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
