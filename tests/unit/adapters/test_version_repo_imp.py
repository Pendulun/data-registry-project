from unittest import TestCase

from src.app.adapters.out.VersionRepoImp import VersionRepoImp
from src.app.domain.entities.version import Version
from tests.fakes import FakeDatabase, assert_parameterized
from tests.fixtures import (
    CREATED_AT,
    DATASET_ID,
    PAYLOAD,
    SQL_PLACEHOLDER,
    VERSION_ID,
    VERSION_NUMBER,
    version_row,
)


class TestVersionRepoImp(TestCase):

    def test_create_version_parametrizado(self):
        db = FakeDatabase()

        VersionRepoImp(db).create_version(
            Version(version_number=PAYLOAD, dataset_id=PAYLOAD))

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (PAYLOAD, PAYLOAD))
        self.assertEqual(db.commits, 1)

    def test_get_version_parametrizado_e_mapeia(self):
        db = FakeDatabase(row=version_row(row_id=VERSION_ID))

        result = VersionRepoImp(db).get_version(PAYLOAD)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (PAYLOAD, ))
        self.assertEqual(
            result,
            Version(id=VERSION_ID,
                    dataset_id=DATASET_ID,
                    version_number=VERSION_NUMBER,
                    created_at=CREATED_AT),
        )

    def test_get_version_retorna_none(self):
        db = FakeDatabase(row=None)

        self.assertIsNone(VersionRepoImp(db).get_version(VERSION_ID))

    def test_get_version_for_dataset_usa_ordem_dataset_version(self):
        db = FakeDatabase(row=version_row())

        result = VersionRepoImp(db).get_version_for_dataset(
            version_number=VERSION_NUMBER, dataset_id=DATASET_ID)

        query, params = db.cursor.calls[0]
        self.assertEqual(query.count(SQL_PLACEHOLDER), 2)
        self.assertEqual(params, (DATASET_ID, VERSION_NUMBER))
        self.assertEqual(result.version_number, VERSION_NUMBER)

    def test_get_version_for_dataset_parametrizado(self):
        db = FakeDatabase(row=None)

        VersionRepoImp(db).get_version_for_dataset(
            version_number=PAYLOAD, dataset_id=DATASET_ID)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (DATASET_ID, PAYLOAD))

    def test_get_version_for_dataset_by_id_usa_ordem_dataset_version(self):
        db = FakeDatabase(row=version_row(row_id=VERSION_ID))

        result = VersionRepoImp(db).get_version_for_dataset_by_id(
            version_id=VERSION_ID, dataset_id=DATASET_ID)

        query, params = db.cursor.calls[0]
        self.assertEqual(query.count(SQL_PLACEHOLDER), 2)
        self.assertEqual(params, (DATASET_ID, VERSION_ID))
        self.assertEqual(result.id, VERSION_ID)

    def test_get_version_for_dataset_by_id_parametrizado(self):
        db = FakeDatabase(row=None)

        VersionRepoImp(db).get_version_for_dataset_by_id(
            version_id=PAYLOAD, dataset_id=DATASET_ID)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(params, (DATASET_ID, PAYLOAD))
