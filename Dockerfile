FROM python:3.7-slim

LABEL website='https://github.com/EISerova/api_yamdb'
LABEL desc='This raiting source create for studing'
LABEL email='katyaserova@yandex.ru'

# Запустить команду создания директории внутри контейнера
RUN mkdir /app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY yamdb/ /app

# Сделать директорию /app рабочей директорией. 
WORKDIR /app

ENV MYSQL_DATABASE raiting_db
ENV MYSQL_USER admin
ENV MYSQL_PASSWORD 12345
ENV MYSQL_ROOT_PASSWORD root

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["python3", "manage.py", "runserver", "0:8000"] 