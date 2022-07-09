import random

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from yamdb.settings import (
    CONFIRMATION_CODE_CHARACTERS,
    CONFIRMATION_CODE_LENGTH,
    EMAIL_HOST_USER,
)


def create_confirmation_code():
    """Создние кода подтверждения."""

    code = ''.join(
        random.choice(CONFIRMATION_CODE_CHARACTERS)
        for _ in range(CONFIRMATION_CODE_LENGTH)
    )
    return code


def send_email(email, confirmation_code, name):
    """Отправка пользователю письма с кодом подтверждения."""

    send_mail(
        'Регистрация на сайте.',
        f'Здравствуйте, {name}, ваш код подтверждения: {confirmation_code}.',
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    """Получение токена для авторизации."""

    access = AccessToken.for_user(user)
    return {'token': str(access)}
