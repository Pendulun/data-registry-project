from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.entities.file import File
from src.app.domain.entities.version import Version
from src.app.ports.out.FileHasher import FileHasher
from src.app.ports.out.FileRepo import FileRepo
from src.app.ports.out.VersionRepo import VersionRepo
from src.app.use_cases.version.upload_file_to_version import UploadFileToVersion
from tests.fixtures import (
    CSV_TYPE,
    DATASET_ID,
    FILE_HASH,
    FILE_PATH,
    VERSION_ID,
    VERSION_NUMBER,
)


class TestUploadFileToVersion(TestCase):

    def setUp(self):
        self.version_repo = Mock(spec=VersionRepo)
        self.file_repo = Mock(spec=FileRepo)
        self.hasher = Mock(spec=FileHasher)
        self.use_case = UploadFileToVersion(
            version_repo=self.version_repo, file_repo=self.file_repo)

    def test_cria_arquivo_quando_versao_existe_e_arquivo_e_novo(self):
        self.version_repo.get_version.return_value = Version(
            version_number=VERSION_NUMBER, dataset_id=DATASET_ID)
        self.file_repo.get_file_by_path_and_version_id.return_value = None
        self.hasher.calculate.return_value = FILE_HASH

        result = self.use_case.execute(version_id=VERSION_ID,
                                       file_hasher=self.hasher,
                                       file_path=FILE_PATH,
                                       file_type=CSV_TYPE)

        self.assertEqual(
            result,
            File(version_id=VERSION_ID,
                 storage_path=FILE_PATH,
                 file_type=CSV_TYPE,
                 hash=FILE_HASH),
        )
        self.version_repo.get_version.assert_called_once_with(
            version_id=VERSION_ID)
        self.file_repo.get_file_by_path_and_version_id.assert_called_once_with(
            file_path=FILE_PATH, version_id=VERSION_ID)
        self.hasher.calculate.assert_called_once_with(FILE_PATH)
        self.file_repo.create_file.assert_called_once()
        self.assertEqual(
            self.file_repo.create_file.call_args.args[0].hash, FILE_HASH)

    def test_retorna_none_quando_versao_nao_existe(self):
        self.version_repo.get_version.return_value = None

        result = self.use_case.execute(version_id=VERSION_ID,
                                       file_hasher=self.hasher,
                                       file_path=FILE_PATH,
                                       file_type=CSV_TYPE)

        self.assertIsNone(result)
        self.file_repo.get_file_by_path_and_version_id.assert_not_called()
        self.hasher.calculate.assert_not_called()
        self.file_repo.create_file.assert_not_called()

    def test_retorna_none_quando_arquivo_ja_existe_na_versao(self):
        self.version_repo.get_version.return_value = Version(
            version_number=VERSION_NUMBER, dataset_id=DATASET_ID)
        self.file_repo.get_file_by_path_and_version_id.return_value = File(
            version_id=VERSION_ID,
            storage_path=FILE_PATH,
            file_type=CSV_TYPE,
            hash=FILE_HASH,
        )

        result = self.use_case.execute(version_id=VERSION_ID,
                                       file_hasher=self.hasher,
                                       file_path=FILE_PATH,
                                       file_type=CSV_TYPE)

        self.assertIsNone(result)
        self.hasher.calculate.assert_not_called()
        self.file_repo.create_file.assert_not_called()
