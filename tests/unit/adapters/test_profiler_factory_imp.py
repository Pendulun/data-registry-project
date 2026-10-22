from unittest import TestCase

from src.app.adapters.out.profiling.csv_profiler import CSVFileProfiler
from src.app.adapters.out.profiling.profiler_factory_imp import (
    FileProfilerFactoryImp,
)
from tests.fixtures import (
    CSV_TYPE,
    PDF_TYPE,
    UNSUPPORTED_TYPE_MESSAGE,
)


class TestFileProfilerFactoryImp(TestCase):

    def setUp(self):
        self.factory = FileProfilerFactoryImp()

    def test_text_csv_retorna_csv_profiler(self):
        self.assertIsInstance(self.factory.get(CSV_TYPE), CSVFileProfiler)

    def test_tipo_desconhecido_levanta_value_error(self):
        with self.assertRaises(ValueError) as context:
            self.factory.get(PDF_TYPE)

        self.assertEqual(str(context.exception), UNSUPPORTED_TYPE_MESSAGE)

    def test_is_valid_para_tipo_suportado(self):
        self.assertTrue(self.factory.is_valid(CSV_TYPE))

    def test_is_valid_para_tipo_nao_suportado(self):
        self.assertFalse(self.factory.is_valid(PDF_TYPE))
