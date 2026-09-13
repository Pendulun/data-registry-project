# application/use_cases/create_dataset.py

from src.app.domain.entities.version import Version
from src.app.ports.out.VersionRepo import VersionRepo


class CreateVersion:

    def __init__(self, repository: VersionRepo):
        self.repository = repository

    def execute(self, version_number: int, dataset_id: int) -> Version:

        if self.repository.get_version_for_dataset(
                version_number=version_number, dataset_id=dataset_id) is None:
            version = Version(version_number=version_number,
                              dataset_id=dataset_id)

            self.repository.create_version(version=version)

            return version
        else:
            return None
