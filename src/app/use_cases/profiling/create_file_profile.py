from src.app.domain.entities.file_profile import FileProfile
from src.app.ports.out.FileRepo import FileRepo
from src.app.ports.out.FileProfilerRepo import FileProfilerRepo
from src.app.ports.out.profiling.FileProfilerFactory import FileProfilerFactory


class CreateFileProfile:

    def __init__(self, file_repo: FileRepo,
                 file_profiler_repo: FileProfilerRepo,
                 profiler_factory: FileProfilerFactory):
        self.file_repo = file_repo
        self.file_profiler_repo = file_profiler_repo
        self.profiler_factory = profiler_factory

    def execute(self, file_id: int) -> FileProfile | None:
        file = self.file_repo.get_file_by_id(file_id)
        if file is None:
            return None

        profiler = self.profiler_factory.get(file.file_type)
        file_profile_result = profiler.calculate(file.storage_path)

        file_profile = FileProfile(file_id=file_id,
                                   n_rows=file_profile_result.n_rows,
                                   n_columns=file_profile_result.n_columns)

        self.file_profiler_repo.create_file_profile(file_profile)

        return file_profile
