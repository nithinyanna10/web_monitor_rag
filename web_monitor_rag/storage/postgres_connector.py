import os
import psycopg2
from psycopg2.extras import RealDictCursor

PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', '1234')
PG_DATABASE = os.getenv('PG_DATABASE', 'postgres')


def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DATABASE
    )

def create_table():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS site_data (
                id SERIAL PRIMARY KEY,
                site VARCHAR(32),
                key VARCHAR(64),
                value TEXT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def insert_data(site, key, value):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            'INSERT INTO site_data (site, key, value) VALUES (%s, %s, %s)',
            (site, key, value)
        )
        conn.commit()

def fetch_data(site=None):
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        if site:
            cur.execute('SELECT * FROM site_data WHERE site=%s ORDER BY ts DESC', (site,))
        else:
            cur.execute('SELECT * FROM site_data ORDER BY ts DESC')
        return cur.fetchall()

if __name__ == '__main__':
    create_table()
    insert_data('site1', 'product', 'Test Product')
    print(fetch_data('site1'))
