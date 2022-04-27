from django.db import models


class Genre(models.Model):
    slug = models.SlugField(
        unique=True,
        db_index=True
    )
    name = models.CharField(
        'Жанр',
        max_length=30
    )
    description = models.CharField(
        'Описание',
        max_length=200
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Название - {self.name}'


class Category(models.Model):
    slug = models.SlugField(
        unique=True,
        db_index=True
    )
    name = models.CharField(
        'Категория',
        max_length=20
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Название - {self.name}'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True
    )
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True
    )
    year = models.IntegerField(
        'Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        blank=False
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        null=True,
        blank=False
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Название - {self.name}'
