import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Genre


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    def handle(self, *args, **kwargs):
        with open('static/data/genre.csv', 'rt', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                try:
                    Genre.objects.get_or_create(id=id, name=name, slug=slug)
                except Exception as error:
                    message = f'Ошибка - {error}, проблема в строке - {row}'
                    raise CommandError(message)

            self.stdout.write('Данные из файла genre.csv перенесены в базу.')
