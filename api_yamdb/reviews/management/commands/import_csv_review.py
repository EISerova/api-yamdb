import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Review


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    def handle(self, *args, **kwargs):
        with open(
            'static/data/review.csv', 'rt', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:
                id = row['id']
                text = row['text']
                title_id = row['title_id']
                author = row['author']
                score = row['score']
                pub_date = row['pub_date']
                try:
                    Review.objects.get_or_create(
                        id=id,
                        text=text,
                        title_id=title_id,
                        author_id=author,
                        score=score,
                        pub_date=pub_date,
                    )
                except Exception as error:
                    message = f'Ошибка - {error}, проблема в строке - {row}'
                    raise CommandError(message)

            self.stdout.write('Данные из файла review.csv перенесены в базу.')
