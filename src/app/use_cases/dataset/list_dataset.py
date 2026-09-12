from typing_extensions import List
from src.app.domain.entities.dataset import Dataset
from src.app.ports.out.DatasetRepo import DatasetRepo


class ListDatasets:

    def __init__(self, repository: DatasetRepo):
        self.repository = repository

    def execute(self) -> List[Dataset]:
        dataset_list = self.repository.get_all_datasets()

        return dataset_list
