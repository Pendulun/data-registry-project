from pydantic import BaseModel


class CreateFileProfileRequest(BaseModel):
    file_id: int
