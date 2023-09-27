import os
from datetime import date

import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()

DB_URL = os.getenv('DATABASE_URL')


def get_all_urls():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            # cur.execute(
            #     '''SELECT u.id, u.name, uc.status_code, uc.created_at
            #     FROM urls AS u
            #     LEFT JOIN
            #         (SELECT DISTINCT ON (url_id) url_id, status_code, created_at
            #             FROM url_checks
            #             ORDER BY url_id, created_at DESC) as uc
            #         ON u.id = uc.url_id
            #     ORDER BY u.id DESC'''
            # )
            cur.execute(
                'SELECT id, name FROM urls ORDER BY id'
            )
            all_urls = cur.fetchall()
            cur.execute(
                '''
                SELECT DISTINCT ON (url_id)
                url_id, status_code, created_at FROM url_checks
                ORDER BY url_id, created_at DESC
                '''
            )
            all_checks = cur.fetchall()
            # print(all_checks)

    # Need an algorithm
    [(1, 'one'), (2, 'two'), (3, 'ten')]
    [(1, 200, 'field'), (3, 202, 'fiels')]
    # End need

    # O(n^2) :-(
    urls = []
    for url in all_urls:
        match = False
        for check in all_checks:
            if url.id in check:
                data = (*url, *check)
                urls.append(data)
                match = True
                break
        if not match:
            urls.append((*url, ))
    print('urls =', urls)

    # urls = [(url, check) for url, check in zip(all_urls, all_checks)]
    return urls
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
