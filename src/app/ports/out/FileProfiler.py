from abc import ABC, abstractmethod

from src.app.domain.value_objects.file_profile_result import FileProfileResult


class FileProfiler(ABC):

    @abstractmethod
    def calculate(self, file_path: str) -> FileProfileResult:
        ...
