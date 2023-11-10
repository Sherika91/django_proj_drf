from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from course.models import Course

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('Member')
    MODERATOR = 'moderator', _('Moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=35, verbose_name='First Name', **NULLABLE, )
    last_name = models.CharField(max_length=35, verbose_name='Last Name', **NULLABLE, )
    phone = models.CharField(max_length=35, verbose_name='Phone', **NULLABLE, )
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE, )
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='Role', )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
