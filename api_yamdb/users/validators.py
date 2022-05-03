from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\z'
