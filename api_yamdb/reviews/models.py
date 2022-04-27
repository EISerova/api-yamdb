from django.db import models
from django.core.validators import RegexValidator

from users.models import User


class Review(models.Model):
    """Модель отзывов."""

    text = models.TextField(
        'текст',
    )
    title_id = models.ForeignKey(
        'произведение', Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        'автор',
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.CharField(
        'оценка',
        max_length=10,
        validators=[
            RegexValidator(r"^\d{1,10}$"),
        ],
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


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField(
        'текст',
    )
    review = models.ForeignKey(
        'отзыв',
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        'автор',
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
