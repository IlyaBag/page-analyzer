import os
from datetime import date
from urllib.parse import urlparse

from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor
import validators


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    url = ''
    errors = {}
    return render_template('index.html', url=url, errors=errors)


@app.post('/urls')
def add_url():
    raw_new_url = request.form.get('url')

    errors = validate_url(raw_new_url)
    if errors:
        return render_template('index.html', url=raw_new_url, errors=errors)

    parsed_new_url = urlparse(raw_new_url)
    new_url = f"{parsed_new_url.scheme}://{parsed_new_url.netloc}"

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                        (new_url, date.today())
                        # (new_url, datetime.strftime(date.today(), '%y-%m-%d'))
                        )
            conn.commit()
            cur.execute(f"SELECT id FROM urls WHERE name='{new_url}'")
            id = cur.fetchone()[0]
    # cur.close()
    # conn.close()
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url_id', id=id))

    # with psycopg2.connect(DSN) as conn:
    # with conn.cursor() as curs:
    #     curs.execute(SQL)
    # ---
    # conn = psycopg2.connect(DSN)

    # with conn:
    #     with conn.cursor() as curs:
    #         curs.execute(SQL1)

    # with conn:
    #     with conn.cursor() as curs:
    #         curs.execute(SQL2)

    # conn.close()


@app.get('/urls')
def show_urls():
    # получить из БД все сохранённые адреса, отсортировать
    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls ORDER BY id DESC')
            all_urls = cur.fetchall()
    # вывести таблицу на страницу
    return render_template('show.html', all_urls=all_urls)


@app.get('/urls/<id>')
def show_url_id(id):
    # получить из БД запись с нужным id
    messages = get_flashed_messages(with_categories=True)
    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(f'SELECT * FROM urls WHERE id=%s', (id,))
            url = cur.fetchone()
    return render_template('url_id.html', url=url, messages=messages)


def validate_url(url):
    errors = {}
    if not url:
        errors['empty url'] = 'URL обязателен'
    elif len(url) > 255:
        errors['long url'] = 'URL превышает 255 символов'
    elif not validators.url(url):
        errors['invalid url'] = 'Некорректный URL'
    return errors
