import psycopg


class Database:

    def __init__(self, dsn: str):
        self.connection = psycopg.connect(dsn)

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
