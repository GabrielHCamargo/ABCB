from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.ticket import create_ticket
from services.ticket import update_ticket


router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_ticket(ticket: Dict, db: AsyncSession = Depends(get_session)): 
    
    new_ticket = await create_ticket(ticket, db)

    return {"msg": new_ticket}


@router.put("/{ticket_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_ticket(ticket_id: int, ticket: Dict, db: AsyncSession = Depends(get_session)):

    ticket = await update_ticket(ticket_id, ticket, db)
    
    return {"msg": ticket}