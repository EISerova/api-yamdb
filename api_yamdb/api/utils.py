import random

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from api_yamdb.settings import (
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


def get_user(username, email):
    """
    Получение пользователя с задаными данными из сериалайзера.
    Возвращает None, если такой не зарегистрирован.
    """

    try:
        user = User.objects.get(username=username, email=email)
        return user
    except User.DoesNotExist:
        return None


def check_username_email(username, email):
    """Проверка наличия пользователей с заданными username или email."""

    username_user = User.objects.filter(username=username).exists()
    email_user = User.objects.filter(email=email.lower()).exists()
    return username_user or email_user
