from typing import List

from sqlmodel import select

from models.event_code import EventCodeModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def events_codes(manipulated_object, event_ocurred, db):
    async with db as session:
        query_events_codes = select(EventCodeModel)
        result_events_codes = await session.execute(query_events_codes)
        events_codes: List[EventCodeModel] = [row[0] for row in result_events_codes.all()]
        
        for code in events_codes:
            if code.manipulated_object == manipulated_object and code.event_ocurred == event_ocurred:
                return code
        
        return None