import random

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken


def create_confirmation_code():
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ''.join(random.choice(alphabet) for i in range(16))
    return code


def send_email(email, confirmation_code, name):
    send_mail(
        'Регистрация на сайте.',
        f'Здравствуйте, {name}, ваш код подтвердждения: {confirmation_code}.',
        'from@example.com',
        [email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    access = AccessToken.for_user(user)
    return {'token': str(access)}
