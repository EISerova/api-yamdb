from django.db import models
from django.core.validators import RegexValidator

from users.models import User
from .validators import validate_score


class Genre(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField('Жанр', max_length=30)
    description = models.CharField('Описание', max_length=200)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Название - {self.name}'


class Category(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField('Категория', max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Название - {self.name}'


class Title(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    description = models.TextField(
        'Описание', max_length=255, null=True, blank=True
    )
    year = models.IntegerField(
        'Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        blank=False,
    )
    genre = models.ManyToManyField(Genre, related_name='titles', blank=False)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Название - {self.name}'


class Review(models.Model):
    """Модель отзывов."""

    text = models.TextField(
        'текст',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField('оценка', validators=[validate_score])
    pub_date = models.DateTimeField(
        'публикации',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return (
            f'текст - {self.text[:15]}'
            f'дата публикации - {self.pub_date}'
            f'автор - {self.author.username}'
            f'произведение - {self.title}'
            f'оценка - {self.score}'
        )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField(
        'текст',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return (
            f'текст - {self.text[:15]}'
            f'дата публикации - {self.pub_date}'
            f'автор - {self.author.username}'
            f'отзыв - {self.review}'
        )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
