from abc import ABC, abstractmethod
from typing_extensions import List

from src.app.domain.entities.file import File


class FileRepo(ABC):

    @abstractmethod
    def create_file(self, file: File):
        pass

    @abstractmethod
    def get_file_by_path_and_version_id(self, file_path: str,
                                        version_id: int) -> File | None:
        pass
