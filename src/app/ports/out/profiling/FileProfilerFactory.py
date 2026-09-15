from abc import ABC, abstractmethod

from src.app.ports.out.FileProfiler import FileProfiler


class FileProfilerFactory(ABC):

    @abstractmethod
    def get(self, file_type: str) -> FileProfiler:
        ...
