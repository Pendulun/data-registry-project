from abc import ABC, abstractmethod

from src.app.domain.entities.dataset import Dataset
from src.app.domain.entities.version import Version


class VersionRepo(ABC):

    @abstractmethod
    def create_version(self, version: Version):
        pass

    @abstractmethod
    def get_version(self, version_id: int) -> Version | None:
        pass

    @abstractmethod
    def get_version_for_dataset(self, version_number: int,
                                dataset_id: int) -> Version | None:
        pass

    @abstractmethod
    def get_version_for_dataset_by_id(self, version_id: int,
                                      dataset_id: int) -> Version | None:
        pass
