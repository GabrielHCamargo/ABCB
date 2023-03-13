from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.customer import update_customer


router = APIRouter()


# PUT Customer 
@router.put("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_customer(customer_id: int, customer: Dict, db: AsyncSession = Depends(get_session)):

    customer = await update_customer(customer_id, customer, db)

    return {"msg": customer}