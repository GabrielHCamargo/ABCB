from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.benefit import update_benefit


router = APIRouter()


# PUT Benefit 
@router.put("/{benefit_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_benefit(benefit_id: int, benefit: Dict, db: AsyncSession = Depends(get_session)):

    benefit = await update_benefit(benefit_id, benefit, db)

    return {"msg": benefit}