from dataclasses import dataclass
import uuid


@dataclass
class Version:
    version_number: int
    id: uuid.UUID = None
    dataset_id: uuid.UUID = None
    created_at: str = None
