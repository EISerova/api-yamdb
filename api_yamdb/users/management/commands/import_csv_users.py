import csv

from django.core.management.base import BaseCommand, CommandError

from users.models import User


class Command(BaseCommand):
    help = 'Запись в БД данных из csv-файлов'

    def handle(self, *args, **kwargs):
        with open('static/data/users.csv', 'rt', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                confirmation_code = row['confirmation_code']

                try:
                    User.objects.get_or_create(
                        id=id,
                        username=username,
                        email=email,
                        role=role,
                        bio=bio,
                        first_name=first_name,
                        last_name=last_name,
                        confirmation_code=confirmation_code,
                    )
                except Exception as error:
                    message = f'Ошибка - {error}, проблема в строке - {row}'
                    raise CommandError(message)

            self.stdout.write('Данные из файла users.csv перенесены в базу.')
