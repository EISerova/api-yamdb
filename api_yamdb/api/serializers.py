from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.settings import CONFIRMATION_CODE_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import RegexUsernameValidator, validate_username_not_me


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и создания пользователей админом."""

    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )
        model = User


class AccountSerializer(UserSerializer):
    """Сериализатор для просмотра юзером своего профиля."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        max_length=150,
        validators=[validate_username_not_me, RegexUsernameValidator],
    )
    email = serializers.EmailField(
        max_length=254, allow_blank=False, allow_null=False
    )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для создания токенов."""

    username = serializers.CharField(
        max_length=150,
        validators=[validate_username_not_me, RegexUsernameValidator],
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по категориям."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по жанрам."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных запросов по произведениям."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        read_only_fields = ('__all__',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для небезопасных запросов по произведениям."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по обзорам."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        """Проверка, что это первый отзыв пользователя на произведение."""
        if self.context.get('request').method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = self.context.get('request').user
        message = 'Вы уже оставляли отзыв на это произведение.'
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(message)
        return data

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по комментариям."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
