from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile

from services.file import process_base
from services.file import process_return
from services.file import process_transfers


from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
# from services.request_event import create_request_events


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router: APIRouter = APIRouter()


@router.post("/bases", status_code=status.HTTP_200_OK)
async def post_file(file: UploadFile):
    
    processed_data = await process_base(file)

    return {"creator_user": "user", "data": processed_data}


@router.post("/returns", status_code=status.HTTP_200_OK)
async def post_file(file: UploadFile):
    
    processed_data = await process_return(file)

    return {"creator_user": "user", "data": processed_data}


@router.post("/transfers", status_code=status.HTTP_200_OK)
async def post_file(file: UploadFile):
    
    processed_data = await process_transfers(file)

    return {"creator_user": "user", "data": processed_data}


@router.post("/documents", status_code=status.HTTP_200_OK)
async def post_file(file: UploadFile):
    
    

    return {"creator_user": "user", "data": "processed_data"}