from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.entities.file import File
from src.app.domain.entities.file_profile import FileProfile
from src.app.domain.value_objects.file_profile_result import FileProfileResult
from src.app.ports.out.FileProfiler import FileProfiler
from src.app.ports.out.FileProfilerRepo import FileProfilerRepo
from src.app.ports.out.FileRepo import FileRepo
from src.app.ports.out.profiling.FileProfilerFactory import FileProfilerFactory
from src.app.use_cases.profiling.create_file_profile import CreateFileProfile
from tests.fixtures import (
    CSV_TYPE,
    FILE_HASH,
    FILE_ID,
    FILE_PATH,
    N_COLUMNS,
    N_ROWS,
    PDF_PATH,
    PDF_TYPE,
    UNSUPPORTED_TYPE_MESSAGE,
    VERSION_ID,
)


class TestCreateFileProfile(TestCase):

    def setUp(self):
        self.file_repo = Mock(spec=FileRepo)
        self.profiler_repo = Mock(spec=FileProfilerRepo)
        self.factory = Mock(spec=FileProfilerFactory)
        self.profiler = Mock(spec=FileProfiler)
        self.use_case = CreateFileProfile(file_repo=self.file_repo,
                                          file_profiler_repo=self.profiler_repo,
                                          profiler_factory=self.factory)

    def test_cria_perfil_quando_arquivo_existe(self):
        self.file_repo.get_file_by_id.return_value = File(
            version_id=VERSION_ID,
            storage_path=FILE_PATH,
            file_type=CSV_TYPE,
            hash=FILE_HASH,
        )
        self.factory.get.return_value = self.profiler
        self.profiler.calculate.return_value = FileProfileResult(
            n_columns=N_COLUMNS, n_rows=N_ROWS)

        result = self.use_case.execute(FILE_ID)

        self.assertEqual(
            result,
            FileProfile(file_id=FILE_ID,
                        n_columns=N_COLUMNS,
                        n_rows=N_ROWS),
        )
        self.file_repo.get_file_by_id.assert_called_once_with(FILE_ID)
        self.factory.get.assert_called_once_with(CSV_TYPE)
        self.profiler.calculate.assert_called_once_with(FILE_PATH)
        self.profiler_repo.create_file_profile.assert_called_once_with(
            FileProfile(file_id=FILE_ID,
                        n_columns=N_COLUMNS,
                        n_rows=N_ROWS))

    def test_retorna_none_quando_arquivo_nao_existe(self):
        self.file_repo.get_file_by_id.return_value = None

        result = self.use_case.execute(FILE_ID)

        self.assertIsNone(result)
        self.factory.get.assert_not_called()
        self.profiler_repo.create_file_profile.assert_not_called()

    def test_propaga_erro_de_tipo_nao_suportado(self):
        self.file_repo.get_file_by_id.return_value = File(
            version_id=VERSION_ID,
            storage_path=PDF_PATH,
            file_type=PDF_TYPE,
            hash=FILE_HASH,
        )
        self.factory.get.side_effect = ValueError(UNSUPPORTED_TYPE_MESSAGE)

        with self.assertRaises(ValueError):
            self.use_case.execute(FILE_ID)

        self.profiler_repo.create_file_profile.assert_not_called()
