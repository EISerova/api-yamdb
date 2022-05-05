import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    TABLES_FOR_SERIES = {
        Title: 'titles.csv',
        Comment: 'comments.csv',
        Review: 'review.csv',
    }

    TABLES_FOR_BULK = {
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
    }

    def review_create(row):
        try:
            Review.objects.get_or_create(
                id=row['id'],
                text=row['text'],
                title_id=row['title_id'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
        except Exception as error:
            message = f'Ошибка - {error}, проблема в строке - {row}'
            raise CommandError(message)

    def comment_create(row):
        try:
            Comment.objects.get_or_create(
                id=row['id'],
                text=row['text'],
                review_id=row['review_id'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
        except Exception as error:
            message = f'Ошибка - {error}, проблема в строке - {row}'
        raise CommandError(message)

    def title_create(row):
        try:
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
        except Exception as error:
            message = f'Ошибка - {error}, проблема в строке - {row}'
            raise CommandError(message)

    MODEL_CREATE_FUNC = {
        'Review': review_create,
        'Comment': comment_create,
        'Title': title_create,
    }

    def handle(self, *args, **kwargs):
        for model, file in self.TABLES_FOR_SERIES.items():
            with open(
                f'static/data/{file}', 'rt', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for name, func in self.MODEL_CREATE_FUNC.items():
                    if model._meta.object_name == name:
                        for row in csv_reader:
                            func(row)

                self.stdout.write(
                    f'Данные из файлов перенесены в базу {model}.'
                )

        for model, file in self.TABLES_FOR_BULK.items():
            with open(
                f'static/data/{file}', 'rt', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                try:
                    model.objects.bulk_create(
                        model(**row) for row in csv_reader
                    )
                except Exception as error:
                    message = f'Ошибка - {error}'
                    raise CommandError(message)

                self.stdout.write(
                    f'Данные из файлов перенесены в базу {model}.'
                )
