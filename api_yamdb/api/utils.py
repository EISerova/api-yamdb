import random

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from api_yamdb.settings import (
    EMAIL_HOST_USER,
    CONFIRMATION_CODE_LENGTH,
    CONFIRMATION_CODE_CHARACTERS,
)


def create_confirmation_code():
    """Создние кода подтверждения."""

    code = ''.join(
        random.choice(CONFIRMATION_CODE_CHARACTERS)
        for i in range(CONFIRMATION_CODE_LENGTH)
    )
    return code


def send_email(email, confirmation_code, name):
    """Отправка пользователю письма с кодом подтверждения."""

    send_mail(
        'Регистрация на сайте.',
        f'Здравствуйте, {name}, ваш код подтвердждения: {confirmation_code}.',
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    """Получение токена для авторизации."""

    access = AccessToken.for_user(user)
    return {'token': str(access)}


def get_user(serializer):
    """
    Получение пользователя с задаными данными из сериалайзера.
    Возвращает None, если такой незарегистрирован.
    """

    try:
        username = serializer.data['username']
        email = serializer.data['email']
        user = User.objects.get(username=username, email=email)
        return user
    except KeyError:
        return None
    except User.DoesNotExist:
        return None
