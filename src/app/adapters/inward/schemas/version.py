from pydantic import BaseModel


class CreateVersionForDataset(BaseModel):
    version_number: int
    dataset_id: int
