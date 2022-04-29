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
    email = models.EmailField(blank=False)
