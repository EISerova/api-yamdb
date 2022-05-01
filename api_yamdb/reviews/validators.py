from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка, что год выхода произведения не позже текущего."""

    if value > datetime.now().year:
        message = f'{value} год еще не наступил. Исправьте значение'
        raise ValidationError(message)
