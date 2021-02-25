import os

import psycopg2

conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
                        password=os.environ.get('POSTGRES_USER'), host=os.environ.get('POSTGRES_HOST'))
cursor = conn.cursor()
