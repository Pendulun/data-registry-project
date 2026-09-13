from typing_extensions import List

from src.app.ports.out.VersionRepo import VersionRepo
from src.app.adapters.out.connection import Database
from src.app.domain.entities.dataset import Dataset
from src.app.domain.entities.version import Version


class VersionRepoImp(VersionRepo):

    def __init__(self, conn: Database):
        self.conn = conn

    def create_version(self, version: Version):
        with self.conn.get_cursor() as cur:
            # As outras informações de versão serão criadas automaticamente no banco
            # como o id e o timestamp
            cur.execute(
                "INSERT INTO version (dataset_id, version_number) VALUES (%s, %s)",
                (version.dataset_id, version.version_number))
            self.conn.commit()

    def get_version_for_dataset(
        self,
        version_number: int,
        dataset_id: int,
    ) -> Version | None:
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute(f"""
                SELECT * FROM version
                WHERE dataset_id = {dataset_id} AND version_number = {version_number}
                LIMIT 1""")

            row = cur.fetchone()

            if row is not None:

                return Version(
                    id=row[0],
                    dataset_id=row[1],
                    version_number=row[2],
                    created_at=row[3],
                )

            return None

    def get_all_versions_for_dataset(self, dataset: Dataset):
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("SELECT * FROM version WHERE dataset_id = %s",
                        (dataset.id, ))

            rows = cur.fetchall()

            return [
                Dataset(
                    id=row[0],
                    name=row[1],
                    created_at=row[2],
                    description=row[3],
                ) for row in rows
            ]
