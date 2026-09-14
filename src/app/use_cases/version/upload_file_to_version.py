# application/use_cases/create_dataset.py

from src.app.domain.entities.file import File
from src.app.ports.out.VersionRepo import VersionRepo
from src.app.ports.out.FileRepo import FileRepo
from src.app.ports.out.FileHasher import FileHasher


class UploadFileToVersion:

    def __init__(self, version_repo: VersionRepo, file_repo: FileRepo):
        self.version_repo = version_repo
        self.file_repo = file_repo

    def execute(
        self,
        version_id: int,
        file_hasher: FileHasher,
        file_path: str,
        file_type: str,
    ) -> File:

        if self._version_exists(version_id=version_id
                                ) and self._file_doesnt_exists_for_version(
                                    version_id=version_id,
                                    file_path=file_path):
            file = File(
                version_id=version_id,
                storage_path=file_path,
                file_type=file_type,
                hash=file_hasher.calculate(file_path),
            )

            self.file_repo.create_file(file)
            return file

        return None

    def _version_exists(self, version_id: int) -> bool:
        return self.version_repo.get_version(version_id=version_id) is not None

    def _file_doesnt_exists_for_version(self, version_id: int,
                                        file_path: str) -> bool:
        return self.file_repo.get_file_by_path_and_version_id(
            file_path=file_path, version_id=version_id) is None
