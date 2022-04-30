from django.core.exceptions import ValidationError


def validate_score(value):
    if 1 < value > 10:
        message = f'{value} - ошибка. Диапазон оценок - от 1 до 10.'
        raise ValidationError(message)
