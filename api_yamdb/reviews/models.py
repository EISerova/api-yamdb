from django.db import models
from users.models import User

from .validators import validate_year


class CategoryGenreModel(models.Model):
    """Базовая модель для классов Category и Genre."""

    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        abstract = True


class Genre(CategoryGenreModel):
    """Модель жанров."""

    name = models.TextField('Название жанра', max_length=256)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Название - {self.name}'


class Category(CategoryGenreModel):
    """Модель категорий."""

    name = models.CharField('Название категории', max_length=256)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Название - {self.name}'


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
    score = models.PositiveSmallIntegerField(
        'оценка',
    )
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
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_connection'
            )
        ]


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
        ordering = ('-pub_date',)
