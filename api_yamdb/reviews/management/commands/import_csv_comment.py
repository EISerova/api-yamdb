import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Comment


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    def handle(self, *args, **kwargs):
        with open(
            'static/data/comments.csv', 'rt', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:
                id = row['id']
                text = row['text']
                review_id = row['review_id']
                author = row['author']
                pub_date = row['pub_date']

                try:
                    Comment.objects.get_or_create(
                        id=id,
                        text=text,
                        review_id=review_id,
                        author_id=author,
                        pub_date=pub_date,
                    )
                except Exception as error:
                    message = f'Ошибка - {error}, проблема в строке - {row}'
                    raise CommandError(message)

            self.stdout.write('Данные из файла comment.csv перенесены в базу.')
