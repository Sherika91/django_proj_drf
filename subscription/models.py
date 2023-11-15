from django.db import models

from course.models import Course
from users.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    is_subscribed = models.BooleanField(verbose_name='Is Subscribed', default=False)

    def __str__(self):
        return f"{self.user}'s subscription to {self.course.name}"

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
