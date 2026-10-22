from unittest import TestCase

from src.app.adapters.out.DatasetRepoImp import DatasetRepoImp
from src.app.domain.entities.dataset import Dataset
from tests.fakes import FakeDatabase, assert_parameterized
from tests.fixtures import (
    CREATED_AT,
    DATASET_DESCRIPTION,
    DATASET_NAME,
    OTHER_CREATED_AT,
    PAYLOAD,
    SECOND_DATASET_NAME,
    dataset_row,
)


class TestDatasetRepoImp(TestCase):

    def test_create_dataset_parametrizado(self):
        db = FakeDatabase()

        DatasetRepoImp(db).create_dataset(
            Dataset(name=PAYLOAD, description=PAYLOAD))

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(db.commits, 1)

    def test_get_dataset_by_name_parametrizado_e_mapeia_linha(self):
        db = FakeDatabase(row=dataset_row())

        result = DatasetRepoImp(db).get_dataset_by_name(PAYLOAD)

        query, params = db.cursor.calls[0]
        assert_parameterized(self, query, params)
        self.assertEqual(
            result,
            Dataset(id=1,
                    name=DATASET_NAME,
                    created_at=CREATED_AT,
                    description=DATASET_DESCRIPTION),
        )

    def test_get_dataset_by_name_retorna_none(self):
        db = FakeDatabase(row=None)

        self.assertIsNone(
            DatasetRepoImp(db).get_dataset_by_name(DATASET_NAME))

    def test_get_all_datasets_mapeia_linhas(self):
        db = FakeDatabase(rows=[
            dataset_row(),
            dataset_row(row_id=2,
                        name=SECOND_DATASET_NAME,
                        created_at=OTHER_CREATED_AT,
                        description=None),
        ])

        result = DatasetRepoImp(db).get_all_datasets()

        self.assertEqual(
            result,
            [
                Dataset(id=1,
                        name=DATASET_NAME,
                        created_at=CREATED_AT,
                        description=DATASET_DESCRIPTION),
                Dataset(id=2,
                        name=SECOND_DATASET_NAME,
                        created_at=OTHER_CREATED_AT,
                        description=None),
            ],
        )
        query, params = db.cursor.calls[0]
        self.assertIn("SELECT", query)
        self.assertIsNone(params)

    def test_get_all_datasets_vazio(self):
        db = FakeDatabase(rows=[])

        self.assertEqual(DatasetRepoImp(db).get_all_datasets(), [])
