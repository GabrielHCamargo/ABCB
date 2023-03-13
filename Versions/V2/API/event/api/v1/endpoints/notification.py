from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.notifications import read_notification
from services.notifications import update_notification


router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def get_notifications(user_id: int, notification_id: int = None, db: AsyncSession = Depends(get_session)):

    notification = await read_notification(user_id, notification_id, db)

    return {"msg": notification}


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def view_notifications(user_id: int, notification_id: int = None, db: AsyncSession = Depends(get_session)):

    notification = await update_notification(user_id, notification_id, db)

    return {"msg": notification}