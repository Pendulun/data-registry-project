"""Fakes compartilhados pelos testes unitários (sem banco)."""

from tests.fixtures import PAYLOAD, SQL_PLACEHOLDER


class FakeCursor:
    """Cursor mínimo que registra as chamadas de ``execute``."""

    def __init__(self, row=None, rows=None):
        self.calls = []
        self.row = row
        self.rows = rows or []

    def execute(self, query, params=None):
        self.calls.append((query, params))

    def fetchone(self):
        return self.row

    def fetchall(self):
        return self.rows

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeDatabase:
    """Substitui ``connection.Database`` sem abrir conexão."""

    def __init__(self, row=None, rows=None):
        self.cursor = FakeCursor(row=row, rows=rows)
        self.commits = 0

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.commits += 1


def assert_parameterized(testcase, query, params, payload=PAYLOAD):
    """Garante que o valor viaja como parâmetro, nunca dentro da query."""
    testcase.assertNotIn(payload, query)
    testcase.assertIn(payload, params)
    testcase.assertEqual(query.count(SQL_PLACEHOLDER), len(params))
