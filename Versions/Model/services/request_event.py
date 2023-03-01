from typing import List

from sqlmodel import select

from models.request_event import RequestEventModel

import datetime


async def create_request_events(db, endpoint, method, creator_user, status):
    async with db as session:
        request_events: RequestEventModel = RequestEventModel(
            endpoint=endpoint,
            method=method,
            creator_user=creator_user,
            creation_date=datetime.date.today(),
            completion_date=None,
            status=status,
        )

        session.add(request_events)
        await session.commit()


async def finished_request_events(db, creator_user, endpoint):
    async with db as session:
        query = select(RequestEventModel).where(RequestEventModel.creator_user == creator_user)
        result = await session.execute(query)
        events: List[RequestEventModel] = result.scalars().all()
        incomplete_events = [e for e in events if e.completion_date is None and e.endpoint == endpoint]
        for e in incomplete_events:
            if e:
                e.completion_date = datetime.date.today()
                e.status = "finished"
        await session.commit()
