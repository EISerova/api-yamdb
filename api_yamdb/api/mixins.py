from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers


class CreateDestroyListMixin(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class UsernameValidationMixin(serializers.BaseSerializer):
    def validate_username(self, value):
        """Запрет на создание пользователя с username - me."""

        if value == 'me':
            raise serializers.ValidationError('Имя пользователя me запрещено.')
        return value
