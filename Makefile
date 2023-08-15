PORT ?= 8000

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer/

check: lint

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
