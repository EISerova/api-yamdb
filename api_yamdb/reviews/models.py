from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import CONFIRMATION_CODE_LENGTH
from .validators import (
    RegexUsernameValidator,
    validate_username_not_me,
    validate_year,
)
from .ulils import get_max_role_length


class User(AbstractUser):
    """Модель пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    max_role_length = get_max_role_length(ROLES)

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexUsernameValidator, validate_username_not_me],
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=max_role_length,
        default=USER,
        blank=False,
        choices=ROLES,
    )
    email = models.EmailField('почта', max_length=254, unique=True)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=CONFIRMATION_CODE_LENGTH, null=True
    )

    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def is_moderator(self):
        return self.role == self.MODERATOR


class CategoryGenreModel(models.Model):
    """Базовый класс для моделей Category и Genre."""

    slug = models.SlugField('Cлаг', max_length=50, unique=True, db_index=True)
    name = models.TextField('Название', max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Название - {self.name}'


class Genre(CategoryGenreModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(CategoryGenreModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведений."""

    name = models.TextField('Название произведения', db_index=True)
    description = models.TextField('Описание', null=True, blank=True)
    year = models.PositiveSmallIntegerField('Год', validators=[validate_year])
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        blank=False,
        verbose_name="категория",
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=False, verbose_name="жанр"
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Название - {self.name}'


class ReviewCommentModel(models.Model):
    """Базовый класс для моделей Review и Comment."""

    text = models.TextField(
        'текст',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор",
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(ReviewCommentModel):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="произведение",
    )
    score = models.PositiveSmallIntegerField(
        'оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    FIELDS_INFO = (
        'Текст: {text};'
        'Дата публикации: {pub_date};'
        'Автор: {author};'
        'Произведение: {title};'
        'Оценка: {score}.'
    )

    def __str__(self):
        return self.FIELDS_INFO.format(
            text=self.text,
            pub_date=self.pub_date,
            author=self.author.username,
            title=self.title,
            score=self.score,
        )

    class Meta(ReviewCommentModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_connection'
            )
        ]


class Comment(ReviewCommentModel):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="обзор",
    )

    FIELDS_INFO = (
        'Текст: {text};'
        'Дата публикации: {pub_date};'
        'Автор: {author};'
        'Обзор: {review};'
    )

    def __str__(self):
        return self.FIELDS_INFO.format(
            text=self.text,
            pub_date=self.pub_date,
            author=self.author.username,
            review=self.review,
        )

    class Meta(ReviewCommentModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
