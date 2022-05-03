from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from api_yamdb.settings import CONFIRMATION_CODE_LENGTH


class DefaultUserSerializer(serializers.ModelSerializer):
    """Базовый сериалайзер для работы с моделью User."""

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


class UserSerializer(DefaultUserSerializer):
    """Сериализатор для просмотра и создания пользователей админом."""

    def validate(self, data):
        """Запрет на создание пользователя с username - me."""

        if data.get('username') == 'me':
            raise serializers.ValidationError('Имя пользователя me запрещено.')
        return data

    class Meta:
        fields = DefaultUserSerializer.Meta.fields
        model = User


class AccountSerializer(DefaultUserSerializer):
    """Сериализатор для просмотра юзером своего профиля."""

    class Meta:
        fields = DefaultUserSerializer.Meta.fields
        read_only_fields = ('role',)
        model = User


class SignUpSerializer(UserSerializer):
    """Сериализатор для регистрации."""

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для создания токенов."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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
