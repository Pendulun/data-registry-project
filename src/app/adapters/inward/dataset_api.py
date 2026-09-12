from fastapi import APIRouter
from pydantic import BaseModel

from src.app.adapters.out import connection, DatasetRepoImp
from src.app.use_cases.dataset.create_dataset import CreateDataset
from src.app.use_cases.dataset.list_dataset import ListDatasets
from src.app.config import settings


class CreateDatasetRequest(BaseModel):
    name: str
    description: str


router = APIRouter()


@router.post("/create/")
def create_dataset(request: CreateDatasetRequest):
    repo = DatasetRepoImp.DatasetRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    new_dataset = CreateDataset(repository=repo).execute(
        request.name, request.description)
    return new_dataset


@router.get("/list")
def list_datasets():
    repo = DatasetRepoImp.DatasetRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    datasets = ListDatasets(repository=repo).execute()
    return datasets
