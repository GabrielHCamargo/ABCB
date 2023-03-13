from fastapi import HTTPException
from fastapi import status

from sqlmodel import select

from models.event import EventModel
from models.user import UserModel

from services.event_code import events_codes
from services.notifications import send_notification

import datetime


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def started_events(event, db):
    event: EventModel = EventModel.parse_obj(event)
    
    event_code = await events_codes(event.manipulated_object, event.event_ocurred, db)
    
    event.event_description = event_code.event_description
    event.creation_date = datetime.date.today()
    event.status = "started"

    async with db as session:
        query_existing_user = select(UserModel).where(UserModel.id == event.user_id)
        result_existing_user = await session.execute(query_existing_user)
        existing_user = result_existing_user.scalar_one_or_none()

        if existing_user:

            session.add(event)
            await session.commit()

            # Notifica o usuário após a criação do evento
            await send_notification(event, db)

            return event
        
        else:
            raise HTTPException(detail="non-existent user", status_code=status.HTTP_404_NOT_FOUND)


async def finished_events(event_id, db):
    async with db as session:
        query = select(EventModel).where(EventModel.id == event_id)
        result = await session.execute(query)
        event: EventModel = result.scalar_one_or_none()

        event.completion_date = datetime.date.today()
        event.status = "finished"

        # Notifica o usuário após a finalização do evento
        await send_notification(event, db)


        await session.commit()

        return "completed request event"
