import warnings
from unittest import TestCase

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fastapi.testclient import TestClient

from main import app
from tests.fixtures import (
    CREATE_DATASET_URL,
    CREATE_VERSION_URL,
    CSV_BYTES,
    CSV_TYPE,
    DATASET_NAME,
    FILE_PROFILE_URL,
    NON_INTEGER_NUMBER,
    NON_NUMERIC_ID,
    PAYLOAD,
    UPLOAD_FILE_NAME,
    UPLOAD_URL,
    VERSION_ID,
)


class TestRequestValidation(TestCase):
    """Valida apenas o que é rejeitado antes do handler tocar no banco."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app, raise_server_exceptions=False)

    def _upload(self, **data):
        return self.client.post(
            UPLOAD_URL,
            data=data,
            files={"file": (UPLOAD_FILE_NAME, CSV_BYTES, CSV_TYPE)},
        )

    def test_version_id_com_sql_injection(self):
        response = self._upload(file_path=UPLOAD_FILE_NAME, version_id=PAYLOAD)

        self.assertEqual(response.status_code, 422)

    def test_version_id_nao_inteiro(self):
        response = self._upload(file_path=UPLOAD_FILE_NAME,
                                version_id=NON_INTEGER_NUMBER)

        self.assertEqual(response.status_code, 422)

    def test_upload_sem_file_path(self):
        response = self._upload(version_id=str(VERSION_ID))

        self.assertEqual(response.status_code, 422)

    def test_create_dataset_sem_description(self):
        response = self.client.post(CREATE_DATASET_URL,
                                    json={"name": DATASET_NAME})

        self.assertEqual(response.status_code, 422)

    def test_add_version_com_dataset_id_invalido(self):
        response = self.client.post(
            CREATE_VERSION_URL,
            json={
                "version_number": 1,
                "dataset_id": NON_NUMERIC_ID,
            })

        self.assertEqual(response.status_code, 422)

    def test_file_profile_com_file_id_invalido(self):
        response = self.client.post(FILE_PROFILE_URL,
                                    json={"file_id": NON_NUMERIC_ID})

        self.assertEqual(response.status_code, 422)
