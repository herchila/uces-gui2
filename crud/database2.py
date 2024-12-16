import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def db_connect():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        print("Base de datos conectada correctamente.")
        return connection
    except Exception as e:
        print(f"[db_connect] Error en la conexión con la base de datos. Error: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    conn = db_connect()
    if not conn:
        raise Exception("[execute_query] Error inesperado en la conexión con la base de datos (None).")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, params or [])
        conn.commit()

        if fetch:
            return cursor.fetchall()
    except Exception as e:
        print(f"[execute_query] Error: {e}")
    finally:
        cursor.close()
        conn.close()

