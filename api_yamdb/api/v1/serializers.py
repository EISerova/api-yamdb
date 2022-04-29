from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                f'Имя пользователя me запрещено.'
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = user.confirmation_code
        if data['confirmation_code'] != confirmation_code:
            raise serializers.ValidationError(
                f'Передан неверный код подтвержления.'
            )
        return data
