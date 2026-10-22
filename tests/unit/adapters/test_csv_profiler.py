from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from src.app.adapters.out.profiling.csv_profiler import CSVFileProfiler
from src.app.domain.value_objects.file_profile_result import FileProfileResult
from tests.fixtures import (
    CSV_HEADER_ONLY,
    CSV_SINGLE_COLUMN,
    CSV_THREE_ROWS,
    N_COLUMNS,
    N_ROWS,
)


class TestCSVFileProfiler(TestCase):

    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.directory = Path(self._tmp.name)

    def _write(self, name: str, content: str) -> Path:
        path = self.directory / name
        path.write_text(content)
        return path

    def test_conta_linhas_e_colunas(self):
        path = self._write("tres_linhas.csv", CSV_THREE_ROWS)

        result = CSVFileProfiler().calculate(str(path))

        self.assertEqual(result,
                         FileProfileResult(n_columns=N_COLUMNS, n_rows=N_ROWS))

    def test_csv_somente_com_cabecalho(self):
        path = self._write("cabecalho.csv", CSV_HEADER_ONLY)

        result = CSVFileProfiler().calculate(str(path))

        self.assertEqual(result,
                         FileProfileResult(n_columns=N_COLUMNS, n_rows=0))

    def test_csv_com_uma_coluna(self):
        path = self._write("uma_coluna.csv", CSV_SINGLE_COLUMN)

        result = CSVFileProfiler().calculate(str(path))

        self.assertEqual(result,
                         FileProfileResult(n_columns=1, n_rows=N_ROWS - 1))

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            CSVFileProfiler().calculate(
                str(self.directory / "nao_existe.csv"))
