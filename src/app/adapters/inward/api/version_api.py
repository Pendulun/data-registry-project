from fastapi import APIRouter, Form, UploadFile
from typing import Annotated

from src.app.adapters.inward.schemas.version import CreateVersionForDataset
from src.app.adapters.out import connection, VersionRepoImp, FileHasherImp, FileRepoImp
from src.app.config import settings
from src.app.use_cases.version.create_version import CreateVersion
from src.app.use_cases.version.upload_file_to_version import UploadFileToVersion

router = APIRouter()


@router.post("/add_version/")
def add_version(version: CreateVersionForDataset):
    repo = VersionRepoImp.VersionRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    new_version = CreateVersion(repository=repo).execute(
        version.version_number, dataset_id=version.dataset_id)
    return new_version


@router.post("/uploadfile/")
async def upload_file_to_dataset_version(
    file: UploadFile,
    file_path: Annotated[str, Form()],
    version_id: Annotated[str, Form()],
):

    version_repo = VersionRepoImp.VersionRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    file_repo = FileRepoImp.FileRepoImp(conn=connection.Database(
        dsn=settings.DSN))
    new_file = UploadFileToVersion(
        version_repo=version_repo, file_repo=file_repo).execute(
            version_id=version_id,
            file_hasher=FileHasherImp.SHA256FileHasher(),
            file_path=file_path,
            file_type=file.content_type,
        )

    return new_file
