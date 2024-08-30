# Posvyat-backend

_Бэкенд сторона сайта для регистрации пользователей на посвят МИЭМ НИУ ВШЭ 2024 (регистрация, трансфер до пансионата, заселение, фракции)._

## Запуск приложения

Из папки `./posvyat/`:

`python manage.py runserver`

## Запуск тестов

Из папки `./posvyat/`:

`python manage.py test`

## Swagger

[Спецификация API](https://www.notion.so/804886d99be743cbba2938c48468cb4c)

## Endpoints

### POST

#### Регистрация

`api/v1/registration`

#### Трансфер

`api/v1/transfer`

#### Расселение

`api/v1/resettlement`

#### Фракции (касты)

`api/v1/factions`

### GET

#### Время трансфера

`api/v1/times`
