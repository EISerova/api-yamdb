
# REST API YaMDB
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

### Описание:
База отзывов на книги и музыку, доступ через API. Пользователи могут делиться мнением, оценивать произведения, смотреть отзывы других. 
Учебный проект, созданный в рамках учебы в Яндекс.Практикуме.

### Техническое описание проекта:
На странице с документацией localhost/redoc/ можно ознакомиться с примерами запросов и ответов на них.

### Зависимости:
Python 3.8  
Django 2.2  
Django rest framework 3.12

## Примеры API-запросов:

#### Получение списка всех произведений

```http
  GET /api/v1/titles/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   | `string` | **Required**. Ваш токен    |

#### Добавление нового отзыва к произведению

```http
  POST /api/v1/titles/{id}/reviews/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`   | `string` | **Required**. Ваш токен           |
| `id`      | `string` | **Required**. Id произведения     |
| `text`    | `string` | **Required**. Текст отзыва        |
| `score`   | `integer` | **Required**. Оценка произведения |


### Регистрация:
Для регистрации пользователь может самостоятельно отправить свой username и email на /auth/signup/. После этого он получает письмо с кодом подтвержения. Далее необходимо получит токен для аутентификации, использовав код и передав его вместе с username по адресу /auth/token/.

### Запуск проекта в Docker

Запустить контейнер
```power shell
  docker-compose up -d --build
```

Импортировать данные из csv
```power shell
  docker-compose exec web python manage.py import_csv
```

### Авторы: 
- [Екатерина Серова](https://github.com/EISerova/),
- [Анна Бакарасова](https://github.com/Bakarasik),
- [Владимир Мазняк](https://github.com/Cognitoid).

### Обратная связь:
Если у вас есть предложения или замечания, пожалуйста, свяжитесь со мной - katyaserova@yandex.ru

### Лицензия:
[MIT](https://choosealicense.com/licenses/mit/)