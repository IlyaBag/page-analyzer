import os
from urllib.parse import urlparse

import page_analyzer.padb as padb
import page_analyzer.url_check as url_check

from flask import (
    Flask, request, render_template, redirect, url_for,
    flash, get_flashed_messages
)
from dotenv import load_dotenv
import validators
import requests


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    url = ''
    errors = {}
    return render_template('index.html', url=url, errors=errors)


@app.get('/urls')
def show_urls():
    # получить из БД все сохранённые адреса
    all_urls = padb.get_all_urls()
    for au in all_urls:
        print('au =', au)
    return render_template('show.html', all_urls=all_urls)


@app.post('/urls')
def add_url():
    # получить адрес, введённый пользователем
    raw_new_url = request.form.get('url')

    # вернуть ошибку если адрес некорректный
    errors = validate_url(raw_new_url)
    if errors:
        return render_template('index.html',
                               url=raw_new_url,
                               errors=errors), 422

    # распарсить введённый адрес и убрать из него лишнее
    parsed_new_url = urlparse(raw_new_url)
    new_url = f"{parsed_new_url.scheme}://{parsed_new_url.netloc}"

    # проверить, что такого адреса нет в базе данных
    new_url_id = padb.get_id_by_url(new_url)
    if new_url_id:
        flash('Страница уже существует', 'success')
        return redirect(url_for('show_url_id', id=new_url_id))
    # записать адрес в базу данных и получить его id
    padb.save_url_to_db(new_url)
    new_url_id = padb.get_id_by_url(new_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url_id', id=new_url_id))


@app.get('/urls/<id>')
def show_url_id(id):
    # получить из БД запись с нужным id
    messages = get_flashed_messages(with_categories=True)
    url, checks = padb.get_data_by_id(id)
    return render_template('url_id.html',
                           url=url,
                           messages=messages,
                           checks=checks)


@app.post('/urls/<id>/checks')
def check_url(id):
    # получить из БД запись с нужным id
    url, _ = padb.get_data_by_id(id)
    # попытаться сделать запрос на выбранный адрес
    try:
        r = requests.get(url.name, timeout=5)
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_id', id=id))
    # получить код ответа, ожидается "200"
    status = r.status_code
    if status != 200:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_id', id=id))
    # распарсить содержимое полученного ответа
    content = r.text
    tags = url_check.url_check(content)

    # записать в БД результат проверки
    padb.save_check_to_db(id, status, *tags)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url_id', id=id))


def validate_url(url):
    errors = {}
    if not url:
        errors['empty url'] = 'URL обязателен'
    elif len(url) > 255:
        errors['long url'] = 'URL превышает 255 символов'
    elif not validators.url(url):
        errors['invalid url'] = 'Некорректный URL'
    return errors
