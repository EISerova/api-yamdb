from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по обзорам."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = (
            'text',
            'title',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('title_id',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по комментариям."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'text',
            'review',
            'author',
            'pub_date',
        )
