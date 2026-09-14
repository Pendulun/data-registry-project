from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class File:
    version_id: int
    storage_path: str
    file_type: str
    hash: str
    # Gerados automaticamente no banco
    id: uuid.UUID | None = None
    created_at: datetime | None = None
