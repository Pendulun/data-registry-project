from src.app.ports.out.VersionRepo import VersionRepo
from src.app.adapters.out.connection import Database
from src.app.domain.entities.version import Version
from src.app.domain.entities.file import File


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

    def get_version(self, version_id: int) -> Version | None:

        query_str = f"""
                    SELECT * from version 
                    WHERE id = {version_id}
                    """
        return self._query_one_row(query_str=query_str)

    def get_version_for_dataset(
        self,
        version_number: int,
        dataset_id: int,
    ) -> Version | None:
        query_str = f"""
                    SELECT * FROM version
                    WHERE dataset_id = {dataset_id} AND version_number = {version_number}
                    LIMIT 1
                    """
        return self._query_one_row(query_str=query_str)

    def get_version_for_dataset_by_id(self, version_id: int,
                                      dataset_id: int) -> Version | None:
        query_str = f"""
                    SELECT * FROM version
                    WHERE dataset_id = {dataset_id} AND id = {version_id}
                    LIMIT 1
                    """
        return self._query_one_row(query_str=query_str)

    def _query_one_row(self, query_str: str, params: tuple = None) -> Version:
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute(query_str, params=params)

            row = cur.fetchone()

            if row is not None:
                return self._build_version_from_row(row)

            return None

    def _build_version_from_row(self, row) -> Version:
        return Version(
            id=row[0],
            dataset_id=row[1],
            version_number=row[2],
            created_at=row[3],
        )
