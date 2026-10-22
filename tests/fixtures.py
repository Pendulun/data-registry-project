"""Constantes e builders compartilhados pelos testes."""

# Entrada maliciosa usada na regressão de SQL injection
PAYLOAD = "1); DROP TABLE dataset; --"
NON_INTEGER_NUMBER = "1.5"
NON_NUMERIC_ID = "abc"
SQL_PLACEHOLDER = "%s"

# Dataset
DATASET_NAME = "vendas"
SECOND_DATASET_NAME = "clientes"
DATASET_DESCRIPTION = "dados de vendas"
OTHER_DESCRIPTION = "outra descrição"

# Version e file
DATASET_ID = 10
VERSION_NUMBER = 2
VERSION_ID = 5
FILE_ID = 7
FILE_PATH = "/tmp/a.csv"
PDF_PATH = "/tmp/a.pdf"
CSV_TYPE = "text/csv"
PDF_TYPE = "application/pdf"
FILE_HASH = "abc123"
UNSUPPORTED_TYPE_MESSAGE = f"Unsupported file type: {PDF_TYPE}"
N_COLUMNS = 2
N_ROWS = 3
CREATED_AT = "2026-01-01"
OTHER_CREATED_AT = "2026-01-02"

# Conteúdo de arquivos
KNOWN_BYTES = b"abc"
EMPTY_BYTES = b""
LARGE_BYTES = b"x" * 20_000
CSV_ONE_ROW = "a,b\n1,2\n"
CSV_THREE_ROWS = "a,b\n1,2\n3,4\n5,6\n"
CSV_HEADER_ONLY = "a,b\n"
CSV_SINGLE_COLUMN = "a\n1\n2\n"
CSV_BYTES = CSV_ONE_ROW.encode()

# API
UPLOAD_FILE_NAME = "a.csv"
UPLOAD_URL = "/uploadfile/"
CREATE_DATASET_URL = "/create/"
CREATE_VERSION_URL = "/add_version/"
FILE_PROFILE_URL = "/file_profile/"


def dataset_row(row_id=1,
                name=DATASET_NAME,
                created_at=CREATED_AT,
                description=DATASET_DESCRIPTION):
    """Linha como o Postgres devolve de ``SELECT * FROM dataset``."""
    return (row_id, name, created_at, description)


def version_row(row_id=1,
                dataset_id=DATASET_ID,
                version_number=VERSION_NUMBER,
                created_at=CREATED_AT):
    """Linha como o Postgres devolve de ``SELECT * FROM version``."""
    return (row_id, dataset_id, version_number, created_at)


def file_row(row_id=1,
             version_id=VERSION_ID,
             storage_path=FILE_PATH,
             file_type=CSV_TYPE,
             file_hash=FILE_HASH,
             created_at=CREATED_AT):
    """Linha como o Postgres devolve de ``SELECT * FROM file``."""
    return (row_id, version_id, storage_path, file_type, file_hash,
            created_at)
