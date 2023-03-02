from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.ticket import create_ticket
from services.ticket import read_ticket
from services.ticket import update_ticket
from services.ticket import del_ticket

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


# POST Ticket
@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_ticket(ticket: Dict, db: AsyncSession = Depends(get_session)): 
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")
    
    new_ticket = await create_ticket(ticket, db)

    return {"msg": new_ticket}


# GET Ticket
@router.get("/{ticket_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")
    
    ticket = await read_ticket(ticket_id, db)

    return {"msg": ticket}


# PUT Ticket
@router.put("/{ticket_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_ticket(ticket_id: int, ticket: Dict, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")

    ticket = await update_ticket(ticket_id, ticket, db)
    
    return {"msg": ticket}


# DELETE Ticket
@router.delete("/{ticket_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")

    ticket = await del_ticket(ticket_id, db)
    
    return {"msg": ticket}