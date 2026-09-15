# adapters/out/profiling/CSVFileProfiler.py

import pandas as pd

from src.app.domain.value_objects.file_profile_result import FileProfileResult


class CSVFileProfiler:

    def calculate(self, file_path: str) -> FileProfileResult:
        df = pd.read_csv(file_path)

        return FileProfileResult(n_columns=len(df.columns), n_rows=len(df))
