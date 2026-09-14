from abc import ABC, abstractmethod


class FileHasher(ABC):

    @abstractmethod
    def calculate(self, file_path: str) -> str:
        ...
