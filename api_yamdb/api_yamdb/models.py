from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField(
        max_length=30, verbose_name="Жанр", verbose_name_plural="Жанры"
    )
    description = models.CharField(
        max_lenth=200,
        verbose_name="Описание",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return {self.name}


class Category(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField(verbose_name="Категория", max_length=20)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return {self.category_name}


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=200, db_index=True
    )
    description = models.TextField(
        "Описание", max_length=255, null=True, blank=True
    )
    year = models.IntegerField(verbose_name="Год", validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория",
        blank=False,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанры",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return {self.genre}
