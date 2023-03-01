from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.request_event import create_request_events
from services.customer import create_customers_with_benefits
from services.customer import update_customers_benefits
from services.customer import create_discounts
from services.customer import create_documents


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()



# POST Customers
@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_customers(customers: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)): 
    background_tasks.add_task(create_request_events, db, "customers", "POST", customers["creator_user"], "started")
    background_tasks.add_task(create_customers_with_benefits, customers, db)

    return {"msg": "processed data"}


# PUT Benefits
@router.put("/benefits", status_code=status.HTTP_200_OK, response_model=Dict)
async def put_benefits(benefits: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    background_tasks.add_task(create_request_events, db, "benefits", "POST", benefits["creator_user"], "started")
    background_tasks.add_task(update_customers_benefits, benefits, db)

    return {"msg": "processed data"}


# POST Discounts
@router.post("/discounts", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_discounts(discounts: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    background_tasks.add_task(create_request_events, db, "discounts", "POST", discounts["creator_user"], "started")
    background_tasks.add_task(create_discounts, discounts, db)

    return {"msg": "processed data"}


# POST Documents
@router.post("/documents", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_documents(documents: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    background_tasks.add_task(create_request_events, db, "documents", "POST", documents["creator_user"], "started")
    background_tasks.add_task(create_documents, documents, db)

    return {"msg": "processed data"}