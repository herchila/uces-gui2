import os
import psycopg2

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


"""
CREATE TABLE polls_question (
    id BIGINT PRIMARY KEY NOT NULL,
    question_text VARCHAR(128) NOT NULL,
)
"""


def connect_db():
    """
    Establece una conexión a la base de datos PostgreSQL

    Returns:
        connection (psycopg2.extension.connection): Objeto de conexión
        None: Si ocurre un error durante la conexión
    """
    try:
        connection = psycopg2.connect(
            DATABASE_URL,
        )
        print("Base de datos conectada.")
        return connection
    except Exception as e:
        print(f"[DATABASE Exception] Error de conexión: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una consulta SQL de forma segura, maneja conexión y cierre.
    - query: La consulta SQL a ejecutar (puede contener marcadores %s).
    - params: Una lista o tupla de parámetros para la consulta.
    - fetch: Si es True, devuelve los resultados (para SELECT).

    Retorna:
        - Una lista de resultados si `fetch=True`.
        - None si no hay resultados o es una consulta no SELECT.
    """
    conn = connect_db()
    if not conn:
        raise Exception("[DATABASE Exception] Error de conexión")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, params or [])
        conn.commit()
        if fetch:
            return cursor.fetchall()  # Devuelve los resultados de SELECT
    finally:
        cursor.close()
        conn.close()
