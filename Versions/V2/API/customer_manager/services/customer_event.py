import datetime

from typing import List

from sqlmodel import select

from models.customer_event_code import CustomerEventCodeModel
from models.customer_event import CustomersEventsModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_customer_event(db, creator_user, customer_id, nb, object, event, requested=None, inss_return=None, status_code=None):

    if inss_return:
        events = [await customers_events(db, "inss_return", status) for status in ["activated", "error", "canceled"]]
    
        async with db as session:
            inss_event = next((inss for inss in events if inss.event_ocurred == status_code.status), None)

            if inss_event:
                new_customer_event = CustomersEventsModel(
                    customer_id=customer_id,
                    nb=nb,
                    manipulated_object=inss_event.manipulated_object,
                    event_ocurred=inss_event.event_ocurred,
                    event_description=inss_event.event_description,
                    creator_user=creator_user,
                    creation_date=datetime.date.today()
                )
            session.add(new_customer_event)
            await session.commit()

        return True
    
    event = await customers_events(db, object, event, requested)

    async with db as session:
        new_customer_event = CustomersEventsModel(
            customer_id=customer_id,
            nb=nb,
            manipulated_object=event.manipulated_object,
            event_ocurred=event.event_ocurred,
            event_description=event.event_description,
            creator_user=creator_user,
            creation_date=datetime.date.today()
        )
        session.add(new_customer_event)
        await session.commit()
    
    return True
        

async def customers_events(db, object, event, requested=None):
    async with db as session:
        query_customer_event_code = select(CustomerEventCodeModel)
        result_customer_event_code = await session.execute(query_customer_event_code)
        customer_event_code: List = result_customer_event_code.all()

        # Crie um dicionário para mapear os valores de "requested" para os valores de "object"
        requested_to_object = {
            "cancel": "ticket_cancel", "reserve": "ticket_reserve", "others": "ticket_others",
            }

        # Obtenha o valor de "object" correspondente ao valor de "requested"
        if requested in requested_to_object:
            object = requested_to_object[requested]

        # Pesquise o objeto correspondente e retorne-o se encontrado
        for customer_event in customer_event_code:
            if customer_event[0].manipulated_object == object and customer_event[0].event_ocurred == event:
                return customer_event[0]

        # Se nenhum objeto correspondente for encontrado, retorne None
        return None