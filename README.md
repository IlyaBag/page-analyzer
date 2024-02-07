### Hexlet tests and linter status:
[![Actions Status](https://github.com/IlyaBag/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/IlyaBag/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/b88d55a4b3f1f8d6dcba/maintainability)](https://codeclimate.com/github/IlyaBag/python-project-83/maintainability)

# Анализатор страниц

Веб-сервис для простой проверки сайтов на SEO-пригодность. Анализатор позволяет сохранять адреса сайтов и парсить их главные страницы, находя в HTML-коде теги `<h1>`, `<title>` и `<meta name="description">`.

Протестировать приложение можно по [этой ссылке](https://page-analyzer-odw5.onrender.com).

## Технологии

- Python
- Poetry
- Flask
- PostgreSQL

## Использование

### Требования

Перед установкой приложения убедитесь, что у вас установлены:

- Менеджер python-пакетов [Poetry](https://python-poetry.org/docs/#installation)
- Клиент базы данных PostgreSQL

### Установка приложения

1. Клонировать репозиторий
```
git clone https://github.com/IlyaBag/python-project-83.git
```
2. Установить зависимости командой
```
make install
```
3. Создать файл с переменными окружения `.env`
```
cp .env_example .env
```
4. Прописать в файле `.env` значения для переменных окружения (`DATABASE_URL` — URL для подключения к вашей базе данных PostgreSQL, `SECRET_KEY` задаётся произвольно)
5. Создать необходимые таблицы в базе данных. Для этого добавить в своё окружение переменную `DATABASE_URL` и выполнить команду
```
make build
```

### Запуск development сервера

Сервер для разработки можно запустить командой
```
make dev
```

### Деплой

При деплое приложение использует сервер Gunicorn. Запустить его можно командой
```
make start
```
