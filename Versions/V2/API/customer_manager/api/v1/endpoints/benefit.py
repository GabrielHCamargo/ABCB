from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
# from services.request_event import create_request_events
from services.benefit import update_benefits
from services.benefit import update_benefit


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


# POST Benefits
@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_benefits(benefits: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "benefits", "POST", benefits["creator_user"], "started")
    
    background_tasks.add_task(update_benefits, benefits, db)

    return {"msg": "processed data"}


# PUT Benefit 
@router.put("/{benefit_id}", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_benefit(benefit_id: int, benefit: Dict, db: AsyncSession = Depends(get_session)):
    # INICIO O EVENTO DE REQUISIÇÃO
    # background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")

    benefit = await update_benefit(benefit_id, benefit, db)

    return {"msg": benefit}