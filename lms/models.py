from django.db import models


class Course(models.Model):
    title = models.CharField(verbose_name='Название курса', max_length=255)
    avatar = models.ImageField(verbose_name='Превью', upload_to='lms/course', blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name='Город', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title', ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.PROTECT, related_name='lessons')
    title = models.CharField(verbose_name='Название урока', max_length=255)
    description = models.TextField(verbose_name='Описание')
    avatar = models.ImageField(verbose_name='Превью', upload_to='lms/lesson/img', blank=True, null=True)
    video = models.FileField(upload_to='lms/lesson/video', blank=True, null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['title', 'course', ]

    def __str__(self):
        return self.title
