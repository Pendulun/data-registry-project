from src.app.adapters.out.connection import Database
from src.app.domain.entities.file_profile import FileProfile
from src.app.ports.out.FileProfilerRepo import FileProfilerRepo


class FileProfilerRepoImp(FileProfilerRepo):

    def __init__(self, conn: Database):
        self.conn = conn

    def create_file_profile(self, file_profile: FileProfile):
        with self.conn.get_cursor() as cur:
            # O id será criado automaticamente no banco
            cur.execute(f"""
                INSERT INTO file_profile (file_id, n_columns, n_rows)
                VALUES ({file_profile.file_id}, {file_profile.n_columns}, {file_profile.n_rows})
                """)
            self.conn.commit()
