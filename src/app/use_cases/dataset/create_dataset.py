# application/use_cases/create_dataset.py

from src.app.domain.entities.dataset import Dataset
from src.app.ports.out.DatasetRepo import DatasetRepo


class CreateDataset:

    def __init__(self, repository: DatasetRepo):
        self.repository = repository

    def execute(self, name: str, description: str) -> Dataset:
        dataset = Dataset(name=name, description=description)

        if self.repository.get_dataset_by_name(name) is None:

            self.repository.create_dataset(dataset)

            return dataset
        else:
            return None
