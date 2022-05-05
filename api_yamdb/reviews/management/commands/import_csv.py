import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Review, Title, Comment, User


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    MODELS_FILES = {
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
    }

    DIFFERENT_FIELDS = {
        Review: ['author', 'author_id'],
        Comment: ['author', 'author_id'],
        Title: ['category', 'category_id'],
    }

    def handle(self, *args, **kwargs):
        for model, file in self.MODELS_FILES.items():
            with open(
                f'static/data/{file}', 'rt', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if model in self.DIFFERENT_FIELDS:
                        row = {
                            k.replace(
                                self.DIFFERENT_FIELDS[model][0],
                                self.DIFFERENT_FIELDS[model][1],
                            ): v
                            for k, v in row.items()
                        }
                    try:
                        model.objects.create(**row)
                    except Exception as error:
                        message = (
                            f'Ошибка - {error}, проблема в строке - {row}'
                        )
                        raise CommandError(message)

                self.stdout.write(
                    f'Данные из файлов перенесены в базу {model}.'
                )
