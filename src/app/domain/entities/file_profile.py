from dataclasses import dataclass


@dataclass
class FileProfile:
    file_id: int
    n_columns: int
    n_rows: int
    # Gerado automaticamente no banco
    id: int | None = None
