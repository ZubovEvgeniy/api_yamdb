# API YaMDb
### Запрос
```
curl -H 'Accept: application/json' http://127.0.0.1:8000/api/v1/titles/
```
### Ответ
``` json
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
```
### Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.
### Возможности
* Регистрируйтесь.
* Создавайте отзывы на любые произведения.
* Делитесь своим мнением в комментариях к другим отзывам.
### Регистрация пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
### Пользовательские роли
* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять любые отзывы и комментарии.
* **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django** — обладет правами администратора (`admin`)
### Технологии
* Python 3.7.0
* Django 2.2.16
* Django DRF 3.12.4
## Запуск проекта в dev-режиме
- В корневой директории проекта создать файл ```.env``` и установить свои значения для ```SECRET_KEY``` и ```DEBUG```
``` python
SECRET_KEY = 'Your_secret_key'
DEBUG = True # for dev-mode
```
### Для Linux систем
- Выполнить `make help` для просмотра всех доступных команд
``` bash
$ make help
```
- Выполнить `make setup` для установки зависимостей и запуска проекта
``` bash
$ make setup
```
### Для Windows систем
- Установить и активировать виртуальное окружение
``` bash
$ python -m venv venv
```
``` bash
$ source venv/Scripts/activate
```
``` bash
$ python -m pip install -U pip
``` 
- Установить зависимости из файла requirements.txt
``` bash
$ pip install -r requirements.txt
```
- В папке с файлом manage.py выполнить миграции:
``` bash
$ python manage.py migrate
```
- Запустить dev-сервер:
``` bash
$ python manage.py runserver
```
## Выгрузка данных из csv файлов в БД
### Порядок выгрузки данных
### Для Linux систем
- Выполнить `make load` для выгрузки данных из csv файлов в БД
``` bash
$ make load
```
### Для Windows систем
1. Таблица **User** файл users.csv
``` python
$ python manage.py load_users_data
```
2. Таблица **Category** файл category.csv
``` python
$ python manage.py load_category_data
```
3. Таблица **Genre** файл genre.csv
``` python
$ python manage.py load_genre_data
```
4. Таблица **Title** файл titles.csv
``` python
$ python manage.py load_title_data
```
5. Таблица **GenreTitle** файл genre_title.csv
``` python
$ python manage.py load_genre_title_data
```
6. Таблица **Review** файл review.csv
``` python
$ python manage.py load_review_data
```
7. Таблица **Comment** файл comments.csv
``` python
$ python manage.py load_comments_data
```
## Команда разработчиков
Евгений Зубов, Найденов Константин, Арслан Ядов

E-mail:
[Evgenij Zubov](mailto:valzubof@yandex.ru?subject=API%20YaMDb), 
[Naidenov Konstantin](mailto:naiden1898@yandex.ru?subject=API%20YaMDb), 
[Arslan Yadov](mailto:arslanyadov@yandex.ru?subject=API%20YaMDb)
