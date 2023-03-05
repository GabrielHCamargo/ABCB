from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel

from services.customer_event import create_customer_event
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_customer(customer_id, customer, db):
    creator_user = customer["creator_user"]

    async with db as session:
        customer_update: CustomerModel = CustomerModel.parse_obj(customer["data"])

        query_existing_customer = select(CustomerModel).where(CustomerModel.id == customer_id)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:
            for field, value in customer_update.dict(exclude_unset=True).items():
                setattr(existing_customer, field, value)
            
            await session.commit()

            query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == customer_id)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.first()
            nb = existing_benefit[0].nb

            # Adiciona evento
            await create_customer_event(db, creator_user, customer_id, nb, "customer", "update")

            return existing_customer

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "discounts")
