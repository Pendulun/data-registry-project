from unittest import TestCase

from src.app.adapters.out.FileProfilerRepoImp import FileProfilerRepoImp
from src.app.domain.entities.file_profile import FileProfile
from tests.fakes import FakeDatabase, assert_parameterized
from tests.fixtures import (
    FILE_ID,
    N_COLUMNS,
    N_ROWS,
    PAYLOAD,
    SQL_PLACEHOLDER,
)


class TestFileProfilerRepoImp(TestCase):

    def test_create_file_profile_parametrizado(self):
        db = FakeDatabase()

        FileProfilerRepoImp(db).create_file_profile(
            FileProfile(file_id=PAYLOAD,
                        n_columns=PAYLOAD,
                        n_rows=PAYLOAD))

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (PAYLOAD, PAYLOAD, PAYLOAD))
        self.assertEqual(db.commits, 1)

    def test_create_file_profile_usa_ordem_file_colunas_linhas(self):
        db = FakeDatabase()

        FileProfilerRepoImp(db).create_file_profile(
            FileProfile(file_id=FILE_ID,
                        n_columns=N_COLUMNS,
                        n_rows=N_ROWS))

        query, params = db.cursor.calls[0]
        self.assertEqual(query.count(SQL_PLACEHOLDER), 3)
        self.assertEqual(params, (FILE_ID, N_COLUMNS, N_ROWS))
