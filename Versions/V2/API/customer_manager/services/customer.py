import datetime

from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel

from models.customer_event import CustomersEventsModel

from services.customer_event import customers_events
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_customer(customer_id, customer, db):
    event_customer = await customers_events(db, "customer", "update")
    creator_user = customer["creator_user"]

    async with db as session:
        customer_update: CustomerModel = CustomerModel.parse_obj(customer["data"])

        query_existing_customer = select(CustomerModel).where(CustomerModel.id == customer_id)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:
            for field, value in customer_update.dict(exclude_unset=True).items():
                setattr(existing_customer, field, value)
            
            query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == existing_customer.id)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.first()

            # Novo evento
            new_customer_event: CustomersEventsModel = CustomersEventsModel(
                customer_id=existing_customer.id,
                nb=existing_benefit[0].nb,
                manipulated_object=event_customer.manipulated_object,
                event_ocurred=event_customer.event_ocurred,
                event_description=event_customer.event_description,
                creator_user=creator_user,
                creation_date=datetime.date.today()
            )
            session.add(new_customer_event)

            await session.commit()

            return existing_customer

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "discounts")
