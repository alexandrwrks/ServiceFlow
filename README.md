# ServiceFlow

Develop system ServiceFlow for automatization process user's request to service.

## Описание проекта

ServiceFLow — REST API разработанный на FastAPI.

Приложение для управления компаниями, иъ услугами, сотрудниками и заказами клиентов.

Проект разрабатывается с целью создания удобной системы для организации работы компаний предоставляющих услуги.
Сервис позволяет управлять информацией о компании, сотрудниках и услугах, а также обрабатывать заказы.

## Стэк технологий

- Python 3.12
- FastAPI
- aiogram
- SQLAlchemy
- TaskIQ
- Redis
- PyJWT
- Pytest
- Argon2
- Alembic
- Docker

## Возможности

- Регистрация новой компании 
- Создание новой компании
- Создание новых сотрудников и отправка приглашения
- Авторизация пользователей
- Получение списка сотрудников, заказов компании
- Получение информации сотрудников, заказов компании
- Создание заявок 
- Автоматизированные тесты

## Основные возможности

- JWT авторизация
- Layered Architecture
- Redis Cache
- Async SQLAlchemy

## Запуск через Docker

```shell
git clone https://github.com/alexandrwrks/ServiceFlow.git

docker compose up -d
```

## Запуск тестов

```shell
pytest
```


