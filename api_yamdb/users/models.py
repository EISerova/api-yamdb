from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('u', 'user'),
        ('m', 'moderator'),
        ('a', 'admin'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=1,
        default='user',
        blank=False,
        choices=ROLES,
    )
    email = models.EmailField(blank=False, null=False, unique=True)
    confirmation_code = models.TextField('Код подтверждения', null=True)

    def is_admin(self):
        return self.role == 'a'

    def is_moderator(self):
        return self.role == 'm'
