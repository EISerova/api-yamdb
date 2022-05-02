from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_score


class Genre(models.Model):
    """Модель жанров."""

    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField('Жанр', max_length=30)
    description = models.CharField('Описание', max_length=200)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Название - {self.name}'


class Category(models.Model):
    """Модель категорий."""

    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField('Категория', max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Название - {self.name}'


class Title(models.Model):
    """Модель произведений."""

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
    )

    class Meta:
        abstract = True


class Review(ReviewCommentModel):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    _REPRESENTATION = '{text}, {pub_date}, {author}, {title}, {score}'.format(
        text='self.text[:15]',
        pub_date='self.pub_date',
        author='self.author.username',
        title='self.title',
        score='self.score',
    )

    def __str__(self):
        return self._REPRESENTATION

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
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
        related_name='comments',
    )

    _REPRESENTATION = '{text}, {pub_date}, {author}, {review}'.format(
        text='self.text[:15]',
        pub_date='self.pub_date',
        author='self.author.username',
        review='self.review',
    )

    def __str__(self):
        return self._REPRESENTATION

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
