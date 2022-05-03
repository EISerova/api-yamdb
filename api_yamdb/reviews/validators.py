from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя по допустимым символам."""

    regex = r'^[\w.@+-]+\z'


def validate_year(value):
    """Проверка, что год выхода произведения не позже текущего."""

    if value > datetime.now().year:
        message = f'{value} год еще не наступил. Исправьте значение.'
        raise ValidationError(message)
