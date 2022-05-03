from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя по допустимым символам."""

    regex = r'^[\w.@+-]+\z'
