from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.entities.version import Version
from src.app.ports.out.VersionRepo import VersionRepo
from src.app.use_cases.version.create_version import CreateVersion
from tests.fixtures import DATASET_ID, VERSION_NUMBER


class TestCreateVersion(TestCase):

    def setUp(self):
        self.repo = Mock(spec=VersionRepo)
        self.use_case = CreateVersion(repository=self.repo)

    def test_cria_versao_quando_nao_existe(self):
        self.repo.get_version_for_dataset.return_value = None

        result = self.use_case.execute(version_number=VERSION_NUMBER,
                                       dataset_id=DATASET_ID)

        self.assertEqual(
            result,
            Version(version_number=VERSION_NUMBER, dataset_id=DATASET_ID),
        )
        self.repo.get_version_for_dataset.assert_called_once_with(
            version_number=VERSION_NUMBER, dataset_id=DATASET_ID)
        self.repo.create_version.assert_called_once()
        self.assertEqual(
            self.repo.create_version.call_args.kwargs["version"],
            Version(version_number=VERSION_NUMBER, dataset_id=DATASET_ID),
        )

    def test_retorna_none_quando_versao_ja_existe(self):
        self.repo.get_version_for_dataset.return_value = Version(
            version_number=VERSION_NUMBER, dataset_id=DATASET_ID)

        result = self.use_case.execute(version_number=VERSION_NUMBER,
                                       dataset_id=DATASET_ID)

        self.assertIsNone(result)
        self.repo.create_version.assert_not_called()
