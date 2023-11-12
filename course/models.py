from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Course Name', )
    preview = models.ImageField(upload_to='courses/', verbose_name='Course Preview', **NULLABLE, )
    description = models.TextField(verbose_name='Course Description', )

    course_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     verbose_name='Course Owner',)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Lesson Name', )
    description = models.TextField(verbose_name='Lesson Description', )
    preview = models.ImageField(upload_to='lessons/', verbose_name='Lesson Preview', **NULLABLE, )
    video = models.URLField(verbose_name='Lesson Video', **NULLABLE, )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson', verbose_name='Course', )
    lesson_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Lesson Owner',)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name='subscription', null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


