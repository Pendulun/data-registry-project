from fastapi import APIRouter

from src.app.adapters.out import connection, FileRepoImp, FileProfilerRepoImp
from src.app.adapters.out.profiling.profiler_factory_imp import FileProfilerFactoryImp
from src.app.adapters.inward.schemas.profile import CreateFileProfileRequest
from src.app.use_cases.profiling.create_file_profile import CreateFileProfile
from src.app.config import settings

router = APIRouter()


@router.post("/file_profile/")
def file_profile(request: CreateFileProfileRequest):
    file_repo = FileRepoImp.FileRepoImp(connection.Database(dsn=settings.DSN))
    file_profiler_repo = FileProfilerRepoImp.FileProfilerRepoImp(
        connection.Database(dsn=settings.DSN))
    profiler_factory = FileProfilerFactoryImp()
    new_file_profile = CreateFileProfile(
        file_repo=file_repo,
        file_profiler_repo=file_profiler_repo,
        profiler_factory=profiler_factory,
    ).execute(request.file_id)
    print(new_file_profile)
    return new_file_profile
