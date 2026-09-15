from abc import ABC, abstractmethod
from typing_extensions import List
from uuid import UUID

from src.app.domain.entities.file_profile import FileProfile


class FileProfilerRepo(ABC):

    @abstractmethod
    def create_file_profile(self, file_profile: FileProfile):
        pass
