from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    username_validator = [UsernameValidator]

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=150,
        default='user',
        blank=False,
        choices=ROLES,
    )
    email = models.EmailField(blank=False, null=False, unique=True)
    confirmation_code = models.TextField('Код подтверждения', null=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        return self.role == 'moderator'
