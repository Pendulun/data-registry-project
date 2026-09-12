from abc import ABC, abstractmethod
from typing_extensions import List

from src.app.domain.entities.dataset import Dataset


class DatasetRepo(ABC):

    @abstractmethod
    def create_dataset(self, dataset: Dataset):
        pass

    @abstractmethod
    def get_dataset_by_name(self, name: str) -> Dataset | None:
        pass

    @abstractmethod
    def get_all_datasets(self) -> List[Dataset]:
        pass
