from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.entities.dataset import Dataset
from src.app.ports.out.DatasetRepo import DatasetRepo
from src.app.use_cases.dataset.list_dataset import ListDatasets
from tests.fixtures import DATASET_NAME, SECOND_DATASET_NAME


class TestListDatasets(TestCase):

    def setUp(self):
        self.repo = Mock(spec=DatasetRepo)
        self.use_case = ListDatasets(repository=self.repo)

    def test_retorna_lista_do_repositorio(self):
        datasets = [
            Dataset(name=DATASET_NAME),
            Dataset(name=SECOND_DATASET_NAME),
        ]
        self.repo.get_all_datasets.return_value = datasets

        result = self.use_case.execute()

        self.assertIs(result, datasets)
        self.repo.get_all_datasets.assert_called_once_with()

    def test_retorna_lista_vazia(self):
        self.repo.get_all_datasets.return_value = []

        self.assertEqual(self.use_case.execute(), [])
