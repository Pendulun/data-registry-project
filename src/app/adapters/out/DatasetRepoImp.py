from typing_extensions import List

from src.app.ports.out.DatasetRepo import DatasetRepo
from src.app.adapters.out.connection import Database
from src.app.domain.entities.dataset import Dataset


class DatasetRepoImp(DatasetRepo):

    def __init__(self, conn: Database):
        self.conn = conn

    def create_dataset(self, dataset: Dataset):
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute(
                "INSERT INTO dataset (name, description) VALUES (%s, %s)",
                (dataset.name, dataset.description))
            self.conn.commit()

    def get_dataset_by_name(self, name: str) -> Dataset | None:
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("SELECT * FROM dataset WHERE name = (%s) LIMIT 1",
                        (name, ))

            row = cur.fetchone()

            if row is not None:

                return Dataset(
                    id=row[0],
                    name=row[1],
                    created_at=row[2],
                    description=row[3],
                )

            return None

    def get_all_datasets(self) -> List[Dataset]:
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("SELECT * FROM dataset")

            rows = cur.fetchall()

            return [
                Dataset(
                    id=row[0],
                    name=row[1],
                    created_at=row[2],
                    description=row[3],
                ) for row in rows
            ]
