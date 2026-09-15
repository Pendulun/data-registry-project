from dataclasses import dataclass


@dataclass(frozen=True)
class FileProfileResult:
    n_columns: int
    n_rows: int
