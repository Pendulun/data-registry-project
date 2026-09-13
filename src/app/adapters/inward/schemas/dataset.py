from pydantic import BaseModel


class CreateDatasetRequest(BaseModel):
    name: str
    description: str
