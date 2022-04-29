# Generated by Django 2.2.16 on 2022-04-28 22:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('slug', models.SlugField(unique=True)),
                (
                    'name',
                    models.CharField(max_length=20, verbose_name='Категория'),
                ),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=30, verbose_name='Жанр')),
                (
                    'description',
                    models.CharField(max_length=200, verbose_name='Описание'),
                ),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        db_index=True, max_length=200, verbose_name='Название'
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name='Описание',
                    ),
                ),
                ('year', models.IntegerField(verbose_name='Год')),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='titles',
                        to='reviews.Category',
                    ),
                ),
                (
                    'genre',
                    models.ManyToManyField(
                        related_name='titles', to='reviews.Genre'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='текст')),
                (
                    'score',
                    models.CharField(
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^\\d{1,10}$'
                            )
                        ],
                        verbose_name='оценка',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='публикации'
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'title_id',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to='reviews.Title',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='текст')),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='дата публикации'
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'review',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='reviews.Review',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
