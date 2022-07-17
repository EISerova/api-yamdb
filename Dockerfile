FROM python:3.7-slim
LABEL website='https://github.com/EISerova/api_yamdb'
LABEL desc='This raiting source create for studing'
LABEL email='katyaserova@yandex.ru'

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/scr/raiting-drf

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /usr/scr/raiting-drf

# EXPOSE 8000
