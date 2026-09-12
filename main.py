import dotenv
from fastapi import FastAPI, Form, UploadFile
from pydantic import BaseModel
from typing import Annotated

from src.app.adapters.inward import dataset_api

dotenv.load_dotenv()

app = FastAPI()

app.include_router(dataset_api.router)

datasets = dict()


class Dataset(BaseModel):
    name: str
    description: str


class Version(BaseModel):
    id: int
    owner: str


class FileUpload(BaseModel):
    dataset: Dataset
    version: Version
    file: UploadFile


@app.post("/add_version/")
def add_version(version: Version, dataset: Dataset):
    print(version)
    dataset_name = dataset.dataset
    if dataset_name not in datasets:
        return {'status': '500', 'error': 'dataset inexistente!'}

    dataset_versions = datasets[dataset_name]

    if version.id in dataset_versions:
        return {'status': '500', 'error': 'versão já existente!'}

    dataset_versions[version.id] = version.owner

    return {"status": "200"}


@app.post("/uploadfile/")
async def upload_file_to_dataset_version(
    file: UploadFile,
    file_label: Annotated[str, Form()],
    dataset: Annotated[str, Form()],
    version_id: Annotated[str, Form()],
):
    if dataset not in datasets:
        return {'status': '500', 'error': 'dataset inexistente!'}

    dataset_versions = datasets[dataset]

    if version_id in dataset_versions:
        return {'status': '500', 'error': 'versão já existente!'}

    return {
        "filename": file.filename,
        'label': file_label,
        'dataset': dataset,
        'version_id': version_id
    }
