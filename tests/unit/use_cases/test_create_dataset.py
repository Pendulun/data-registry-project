from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.entities.dataset import Dataset
from src.app.ports.out.DatasetRepo import DatasetRepo
from src.app.use_cases.dataset.create_dataset import CreateDataset
from tests.fixtures import (
    DATASET_DESCRIPTION,
    DATASET_NAME,
    OTHER_DESCRIPTION,
)


class TestCreateDataset(TestCase):

    def setUp(self):
        self.repo = Mock(spec=DatasetRepo)
        self.use_case = CreateDataset(repository=self.repo)

    def test_cria_dataset_quando_nome_nao_existe(self):
        self.repo.get_dataset_by_name.return_value = None

        result = self.use_case.execute(DATASET_NAME, DATASET_DESCRIPTION)

        self.assertEqual(
            result,
            Dataset(name=DATASET_NAME, description=DATASET_DESCRIPTION),
        )
        self.repo.get_dataset_by_name.assert_called_once_with(DATASET_NAME)
        self.repo.create_dataset.assert_called_once()
        created = self.repo.create_dataset.call_args.args[0]
        self.assertEqual(created.name, DATASET_NAME)
        self.assertEqual(created.description, DATASET_DESCRIPTION)

    def test_retorna_none_quando_nome_ja_existe(self):
        self.repo.get_dataset_by_name.return_value = Dataset(
            name=DATASET_NAME)

        result = self.use_case.execute(DATASET_NAME, OTHER_DESCRIPTION)

        self.assertIsNone(result)
        self.repo.create_dataset.assert_not_called()
