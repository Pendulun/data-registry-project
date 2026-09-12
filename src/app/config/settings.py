import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("PGSQL_HOST")
POSTGRES_USER = os.getenv("PGSQL_USER")
POSTGRES_DBNAME = os.getenv("PGSQL_DATABASE")
POSTGRES_PWD = os.getenv("PGSQL_PASSWORD")
DSN = f"host={POSTGRES_HOST} dbname={POSTGRES_DBNAME} user={POSTGRES_USER} password={POSTGRES_PWD}"
