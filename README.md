
# API_YaMDb

REST API для социальной сети блогеров Yatube.

## Описание

Проект отзывов YaMDb в рамках обучения на Яндекс Практикум. Благодаря этому проекту можно оставлять отзывы на произведения в различных категориях (например -книги, фильмы, музыка). Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и оценивают произведение по шкале от 1 до 10. Исходя из среднего значения оценое формируется рейтинг произведения. На одно произведение уникальный пользователь может оставить только один отзыв.

## Характеристики

Аутентификация по JWT-токену

Работает со всеми модулями социальной YaMDb: произведениями, отзывами, категориями, жанрами, комментариями.

Получение списка всех категорий, добавление новой категории, удаление категории.

Получение списка всех жанров, добавление жанра, удаление жанра.

Получение списка всех произведений, добавление произведения, удаление произведения.

Получение информации о произведении, частичное обновление информации о произведении.

Получение списка всех отзывов, добавление нового отзыва, полуение отзыва по id.

Частичное обновление отзыва по id, удаление отзыва по id.

Получение списка всех комментариев к отзыву, добавление комментария к отзыву, получение комментария к отзыву.

Частичное обновление комментария к отзыву, удаление комментария к отзыву.

Получение списка всех пользователей, добавление пользователя, получение пользователя по username.

Изменение данных пользователя по username, удаление пользователя по username.

Получение данных своей учетной записи, Изменение данных своей учетной записи.

Поддерживает методы GET, POST, PUT, PATCH, DELETE

Предоставляет данные в формате JSON


## Стек технологий

- Django REST Framework v.3.12.4- написание проекта на Python v.3.7+
- Simple JWT(djangorestframework-simplejwt v.4.7.2) - работа с JWT-токеном
- Git v.2.35.1 - управление версиями

## Подготовка ПО

### Инструкция для Windows

Установите программное обеспечение: скачайте установочные файлы и запустите их.

Python: https://python.org/downloads/

Visual Studio Code: https://visualstudio.com/download/

Git: https://git-scm.com/download/win/

## Запуск проекта

1) После установки ПО откройте VSCode и откройте терминал (Терминал - Создать терминал). Внизу спаправа нажмите `+` и выберите Git Bash (если предпочитаете пользоваться стандартной командной строкой powershell, то используйте их).

2) В командной строке войдите в директорию, где планируете развернуть проект. Например:
```
cd /c/Dev/
```
3) Необходимо склонировать репозитарий проекта:
```
git clone https://github.com/Oleg-Pikalov/api_yamdb.git
```
Теперь ваш проект будет храниться в дериктории например: `/c/Dev/api_yamdb`
Все дальнейшние операции проводятся в дериктории вашего проекта.

4) Установить и активировать виртуальное окружение:
```
python3 -m venv venv            (для Linux и macOS)
source venv/bin/activate        (для Linux и macOS)

python -m venv venv             (для Windows)
sourse venv/Scripts/activate    (для Windows)

```
5) Установить необходимые зависимости:
```
pip install -r requirements.txt
```
6) Выполните миграции(нужно перейти в директорию, где лежит файл manage.py, например -`/c/Dev/api_yamdb/api_yamdb`):
```
python3 manage.py makemigrations  (для Linux и macOS)
python3 manage.py migrate         (для Linux и macOS)

python manage.py makemigrations   (для Windows)
python manage.py migrate          (для Windows)
```
7) Выполните импорт данных:
```
python manage.py import_csv
```
8) Создайте суперпользователя:
```
python3 manage.py createsuperuser (для Linux и macOS)
python manage.py createsuperuser  (для Windows-систем)
```
9) Запустите сервер:
```
python3 manage.py runserver (для Linux и macOS)
python manage.py runserver  (для Windows-систем)
```
Ваш проект запустился на `http://127.0.0.1:8000/`

С помощью команды *pytest* вы можете запустить тесты и проверить работу модулей

C помощью *flake8* вы можете проверить оформление кода

10) Можно создать пользователя после запуска проекта:
```
http://127.0.0.1:8000/v1/auth/signup/
```
отправить POST-запрос:

    {
        "username": "XXXXX",
        "email": "XXXXX"
    }

## Аутентификация

Выполните POST-запрос *localhost:8000/v1/auth/token/* передав поля username и confirmation_code(см. пункт 9 ).

API вернет JWT-токен в формате:

    {
        "token": "ХХХХХXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    }
    
token - наш токен, который необходимо передать в заголовке Authorization: Bearer <токен> при отправке запросов

Теперь пользователь считается авторизованным и может полноценно использовать текущий проект по отзывам произведений.

## Примеры запросов

### Регистрация пользователей и выдача токенов

Регистрация нового пользователя

Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```
Пример запроса:
```
{
"email": "string",
"username": "string"
}
```
Пример ответа:
```
{
"email": "string",
"username": "string"
}
```
Получение JWT-токена

Получение JWT-токена в обмен на username и confirmation code.
Права доступа: Доступно без токена.
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```
Пример запроса:
```
{
"username": "string",
"confirmation_code": "string"
}
```
Пример ответа:
```
{
  "token": "string"
}
```
### Категории

Получение списка всех категорий

Получить список всех категорий
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/categories/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление новой категории

Создать категорию.
Права доступа: Администратор.
Поле slug каждой категории должно быть уникальным.
```
POST http://127.0.0.1:8000/api/v1/categories/
```
Пример запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории

Удалить категорию.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

### Жанры
Получение списка всех жанров

Получить список всех жанров.
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/genres/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление жанра

Добавить жанр.
Права доступа: Администратор.
Поле slug каждого жанра должно быть уникальным.
```
POST http://127.0.0.1:8000/api/v1/genres/
```
Пример запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление жанра

Удалить жанр.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

### Произведения (Titles)
Получение списка всех произведений

Получить список всех объектов.
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
Добавление произведения

Добавить новое произведение.
Права доступа: Администратор.
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
При добавлении нового произведения требуется указать уже существующие категорию и жанр.
```
POST http://127.0.0.1:8000/api/v1/titles/
```
Пример запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Получение информации о произведении

Информация о произведении
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Частичное обновление информации о произведении

Обновить информацию о произведении
Права доступа: Администратор
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
Пример запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Удаление произведения

Удалить произведение.
Права доступа: Администратор.
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

### Отзывы (Reviews)
Получение списка всех отзывов

Получить список всех отзывов.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
Добавление нового отзыва

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
Права доступа: Аутентифицированные пользователи.
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Полуение отзыва по id

Получить отзыв по id для указанного произведения.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частичное обновление отзыва по id

Частично обновить отзыв по id.
Права доступа: Автор отзыва, модератор или администратор.
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление отзыва по id

Удалить отзыв по id
Права доступа: Автор отзыва, модератор или администратор.
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Комментарии к отзывам (Comments)
Получение списка всех комментариев к отзыву

Получить список всех комментариев к отзыву по id
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
Добавление комментария к отзыву

Добавить новый комментарий для отзыва.
Права доступа: Аутентифицированные пользователи.
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Пример запроса:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Получение комментария к отзыву

Получить комментарий для отзыва по id.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частичное обновление комментария к отзыву

Частично обновить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример запроса:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление комментария к отзыву

Удалить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

### Пользователи (Users)
Получение списка всех пользователей

Получить список всех пользователей.
Права доступа: Администратор
```
GET http://127.0.0.1:8000/api/v1/users/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
Добавление пользователя

Добавить нового пользователя.
Права доступа: Администратор
Поля email и username должны быть уникальными
```
POST http://127.0.0.1:8000/api/v1/users/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Получение пользователя по username

Получить пользователя по username.
Права доступа: Администратор
```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Изменение данных пользователя по username

Изменить данные пользователя по username.
Права доступа: Администратор.
Поля email и username должны быть уникальными.
```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Удаление пользователя по username

Удалить пользователя по username.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
```
Получение данных своей учетной записи

Получить данные своей учетной записи
Права доступа: Любой авторизованный пользователь
```
GET http://127.0.0.1:8000/api/v1/users/me/
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Изменение данных своей учетной записи

Изменить данные своей учетной записи
Права доступа: Любой авторизованный пользователь
Поля email и username должны быть уникальными.
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```




Авторы

Владислав Шадрин
Никита Воронков
Олег Пикалов