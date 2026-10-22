import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from src.app.adapters.out.FileHasherImp import SHA256FileHasher
from tests.fixtures import EMPTY_BYTES, KNOWN_BYTES, LARGE_BYTES


class TestSHA256FileHasher(TestCase):

    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.directory = Path(self._tmp.name)

    def _write(self, name: str, content: bytes) -> Path:
        path = self.directory / name
        path.write_bytes(content)
        return path

    def test_hash_de_conteudo_conhecido(self):
        path = self._write("conhecido.bin", KNOWN_BYTES)

        result = SHA256FileHasher().calculate(str(path))

        self.assertEqual(result, hashlib.sha256(KNOWN_BYTES).hexdigest())

    def test_hash_de_arquivo_vazio(self):
        path = self._write("vazio.bin", EMPTY_BYTES)

        result = SHA256FileHasher().calculate(str(path))

        self.assertEqual(result, hashlib.sha256(EMPTY_BYTES).hexdigest())

    def test_hash_de_arquivo_maior_que_o_chunk(self):
        path = self._write("grande.bin", LARGE_BYTES)

        result = SHA256FileHasher().calculate(str(path))

        self.assertEqual(result, hashlib.sha256(LARGE_BYTES).hexdigest())

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            SHA256FileHasher().calculate(
                str(self.directory / "nao_existe.bin"))
