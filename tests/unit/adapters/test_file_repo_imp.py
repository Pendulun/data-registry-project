from unittest import TestCase

from src.app.adapters.out.FileRepoImp import FileRepoImp
from src.app.domain.entities.file import File
from tests.fakes import FakeDatabase, assert_parameterized
from tests.fixtures import (
    CREATED_AT,
    CSV_TYPE,
    FILE_HASH,
    FILE_ID,
    FILE_PATH,
    PAYLOAD,
    SQL_PLACEHOLDER,
    VERSION_ID,
    file_row,
)


class TestFileRepoImp(TestCase):

    def test_create_file_parametrizado(self):
        db = FakeDatabase()

        FileRepoImp(db).create_file(
            File(version_id=PAYLOAD,
                 storage_path=PAYLOAD,
                 file_type=PAYLOAD,
                 hash=PAYLOAD))

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(query.count(SQL_PLACEHOLDER), 4)
        self.assertEqual(db.commits, 1)

    def test_get_file_by_path_and_version_id_parametrizado_e_mapeia(self):
        db = FakeDatabase(row=file_row())

        result = FileRepoImp(db).get_file_by_path_and_version_id(
            PAYLOAD, PAYLOAD)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (PAYLOAD, PAYLOAD))
        self.assertEqual(
            result,
            File(id=1,
                 version_id=VERSION_ID,
                 storage_path=FILE_PATH,
                 file_type=CSV_TYPE,
                 hash=FILE_HASH,
                 created_at=CREATED_AT),
        )

    def test_get_file_by_path_and_version_id_retorna_none(self):
        db = FakeDatabase(row=None)

        self.assertIsNone(
            FileRepoImp(db).get_file_by_path_and_version_id(
                FILE_PATH, VERSION_ID))

    def test_get_file_by_id_parametrizado_e_mapeia(self):
        db = FakeDatabase(row=file_row())

        result = FileRepoImp(db).get_file_by_id(PAYLOAD)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (PAYLOAD, ))
        self.assertEqual(result.id, 1)
        self.assertEqual(result.hash, FILE_HASH)

    def test_get_file_by_id_retorna_none(self):
        db = FakeDatabase(row=None)

        self.assertIsNone(FileRepoImp(db).get_file_by_id(FILE_ID))
