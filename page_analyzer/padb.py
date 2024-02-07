import os
from datetime import date

import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()

DB_URL = os.getenv('DATABASE_URL')


def _get_all_urls_and_checks():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT id, name FROM urls ORDER BY id')
            all_urls = cur.fetchall()

            cur.execute(
                '''
                SELECT DISTINCT ON (url_id)
                url_id, created_at, status_code FROM url_checks
                ORDER BY url_id, created_at DESC
                '''
            )
            all_checks = cur.fetchall()
    return all_urls, all_checks


def get_urls_list():
    # all_urls_example = [(1, 'one'), (2, 'two'), (4, 'ten')]
    # all_checks_example = [(1, 'date1', 200), (4, 'date2', 302)]
    all_urls, all_checks = _get_all_urls_and_checks()
    urls_list = []
    all_checks_position = 0
    for url in all_urls:
        check = ('', '')
        current_check = all_checks[all_checks_position]
        if url.id == current_check.url_id:
            check = current_check[1:]  # first 'url_id' field is redundant
            all_checks_position += 1
        urls_list.append((*url, *check))
    return urls_list

    # cur.close()
    # conn.close()


def get_id_by_url(url):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
            url_id = cur.fetchone()
            return url_id[0] if url_id else None


def get_data_by_id(id):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id=%s', (id,))
            url = cur.fetchone()
            cur.execute('SELECT * FROM url_checks WHERE url_id=%s', (id,))
            checks = cur.fetchall()
            return url, checks


def save_url_to_db(url):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                (url, date.today())
            )
            conn.commit()


def save_check_to_db(id, status, tag_h1, tag_title, tag_meta_descr):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''INSERT INTO url_checks (
                    url_id, status_code, h1, title, description, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)''',
                (id, status, tag_h1, tag_title, tag_meta_descr, date.today())
            )
            conn.commit()
