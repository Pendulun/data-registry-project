from src.app.adapters.out.connection import Database
from src.app.domain.entities.file import File
from src.app.ports.out.FileRepo import FileRepo


class FileRepoImp(FileRepo):

    def __init__(self, conn: Database):
        self.conn = conn

    def create_file(self, file: File):
        with self.conn.get_cursor() as cur:
            # As outras informações de versão serão criadas automaticamente no banco
            # como o id e o timestamp
            cur.execute(
                f"""
                INSERT INTO file (version_id, storage_path, file_type, hash) 
                VALUES ({file.version_id}, %s, %s, %s)
                """, (file.storage_path, file.file_type, file.hash))
            self.conn.commit()

    def get_file_by_path_and_version_id(self, file_path: str,
                                        version_id: int) -> File | None:
        query_str = f"""
                    SELECT * FROM file
                    WHERE storage_path = %s
                        AND version_id = {version_id}
                    LIMIT 1
                    """
        params = (file_path, )
        return self._query_one_row(query_str=query_str, params=params)

    def _query_one_row(self, query_str: str, params: tuple = None) -> File:
        with self.conn.get_cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute(query_str, params=params)

            row = cur.fetchone()

            if row is not None:
                return self._build_file_from_row(row)

            return None

    def _build_file_from_row(self, row) -> File:
        return File(id=row[0],
                    version_id=row[1],
                    storage_path=row[2],
                    file_type=row[3],
                    hash=row[4],
                    created_at=row[5])
