from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
# from services.request_event import create_request_events
from services.customer import read_customer


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


@router.get("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")
    
    customer = await read_customer(customer_id, db)

    return {"msg": customer}