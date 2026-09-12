from dataclasses import dataclass
import uuid


@dataclass
class Dataset:
    name: str
    id: uuid.UUID = None
    created_at: str = None
    description: str | None = None
