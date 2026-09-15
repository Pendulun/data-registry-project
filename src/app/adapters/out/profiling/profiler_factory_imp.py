from src.app.ports.out.FileProfiler import FileProfiler
from src.app.adapters.out.profiling.csv_profiler import CSVFileProfiler
from src.app.ports.out.profiling.FileProfilerFactory import FileProfilerFactory


class FileProfilerFactoryImp(FileProfilerFactory):

    TYPE_TO_PROFILER_MAP = {"text/csv": CSVFileProfiler()}

    def get(self, file_type: str) -> FileProfiler:
        profiler = self.TYPE_TO_PROFILER_MAP.get(file_type, None)
        if profiler is not None:
            return profiler

        raise ValueError(f"Unsupported file type: {file_type}")

    def is_valid(self, file_type: str) -> bool:
        return file_type in self.TYPE_TO_PROFILER_MAP.keys()
