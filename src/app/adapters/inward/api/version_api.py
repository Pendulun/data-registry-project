from fastapi import APIRouter

from src.app.adapters.inward.schemas.version import CreateVersionForDataset
from src.app.adapters.inward.schemas.dataset import CreateDatasetRequest
from src.app.adapters.out import connection, VersionRepoImp
from src.app.config import settings
from src.app.use_cases.version.create_version import CreateVersion

router = APIRouter()


@router.post("/add_version/")
def add_version(version: CreateVersionForDataset):
    repo = VersionRepoImp.VersionRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    new_version = CreateVersion(repository=repo).execute(
        version.version_number, dataset_id=version.dataset_id)
    return new_version
