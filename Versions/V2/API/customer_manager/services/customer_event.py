from typing import List

from sqlmodel import select

from models.customer_event_code import CustomerEventCodeModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


import datetime



async def customers_events(db, object, event):
    async with db as session:
        query_customer_event_code = select(CustomerEventCodeModel)
        result_customer_event_code = await session.execute(query_customer_event_code)
        customer_event_code: List = result_customer_event_code.all()

        for customer_event in customer_event_code:
            if customer_event[0].manipulated_object == object and customer_event[0].event_ocurred == event:
                return customer_event[0]
        return None
        
