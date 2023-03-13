from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.event import started_events
from services.event import finished_events


router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_request_event(event: Dict, db: AsyncSession = Depends(get_session)):
    
    event = await started_events(event, db)

    return {"msg": event}


@router.delete("/{event_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def delete_request_event(event_id: int, db: AsyncSession = Depends(get_session)):
    
    event = await finished_events(event_id, db)

    return {"msg": event}