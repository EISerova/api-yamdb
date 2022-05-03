import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Review, Title, Comment, User


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    FILES = {
        Title: 'titles.csv',
        Comment: 'comments.csv',
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
        Review: 'review.csv',
    }

    def handle(self, *args, **kwargs):
        for model, file in self.FILES.items():
            with open(
                f'static/data/{file}', 'rt', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file)

                if model._meta.object_name == 'Review':
                    for row in csv_reader:
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
                            message = (
                                f'Ошибка - {error}, проблема в строке - {row}'
                            )
                            raise CommandError(message)

                elif model._meta.object_name == 'Comment':
                    for row in csv_reader:
                        try:
                            Comment.objects.get_or_create(
                                id=row['id'],
                                text=row['text'],
                                review_id=row['review_id'],
                                author_id=row['author'],
                                pub_date=row['pub_date'],
                            )
                        except Exception as error:
                            message = (
                                f'Ошибка - {error}, проблема в строке - {row}'
                            )
                            raise CommandError(message)

                elif model._meta.object_name == 'Title':
                    for row in csv_reader:
                        try:
                            model.objects.get_or_create(
                                id=row['id'],
                                name=row['name'],
                                year=row['year'],
                                category_id=row['category'],
                            )
                        except Exception as error:
                            message = (
                                f'Ошибка - {error}, проблема в строке - {row}'
                            )
                            raise CommandError(message)

                elif model._meta.object_name == 'Review':
                    for row in csv_reader:
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
                            message = (
                                f'Ошибка - {error}, проблема в строке - {row}'
                            )
                            raise CommandError(message)

                else:
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
