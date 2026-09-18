import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
POSTGRES_PWD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DSN = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DBNAME} user={POSTGRES_USER} password={POSTGRES_PWD}"
