import dotenv
from fastapi import FastAPI, Form, UploadFile
from pydantic import BaseModel
from typing import Annotated

from src.app.adapters.inward.api import dataset_api
from src.app.adapters.inward.api import version_api

dotenv.load_dotenv()

app = FastAPI()

app.include_router(dataset_api.router)
app.include_router(version_api.router)
