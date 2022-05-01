from django.core.exceptions import ValidationError


def validate_score(value):
    """Проверка, что оценка произведения в диапазоне от 1 до 10."""
    if value < 1 or value > 10:
        message = f'{value} - ошибка. Диапазон оценок - от 1 до 10.'
        raise ValidationError(message)
