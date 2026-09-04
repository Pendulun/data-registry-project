import psycopg
import os

DB_NAME = os.getenv("PGSQL_DATABASE")
DB_HOST = os.getenv("PGSQL_HOST")
DB_USER = os.getenv("PGSQL_USER")
DB_PASSWORD = os.getenv("PGSQL_PASSWORD")

DBS = F"dbname={DB_NAME} host={DB_HOST} user={DB_USER} password={DB_PASSWORD}"


def get_databases():
    result = list()
    with psycopg.connect(DBS) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                SELECT * FROM dataset
                """)
            result = cur.fetchall()

    return result


def add_dataset(name: str, description: str):
    with psycopg.connect(DBS) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute(
                "INSERT INTO dataset (name, description) VALUES (%s, %s)",
                (name, description))
            conn.commit()
