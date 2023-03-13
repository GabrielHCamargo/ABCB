from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.event import EventModel
from models.notification import NotificationModel

import datetime


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def send_notification(event: EventModel, db: AsyncSession):
    async with db as session:
        query = select(NotificationModel).where(NotificationModel.event_id == event.id)
        result = await session.execute(query)
        notification: NotificationModel = result.scalar_one_or_none()

        if notification:
            notification.status = event.status
            notification.creation_date = datetime.date.today()
            notification.visualized = False

            await session.commit()

            return True

        notification: NotificationModel = NotificationModel(
            user_id=event.user_id,
            event_id=event.id,
            message=event.event_description,
            creation_date=datetime.date.today(),
            status=event.status,
            visualized=False,
        )

        session.add(notification)
        await session.commit()

    return True


async def read_notification(user_id, notification_id, db: AsyncSession):
    notification = None

    async with db as session:
        if notification_id is None:
            query = (
                select(NotificationModel)
                .where(NotificationModel.user_id == user_id)
                .order_by(NotificationModel.creation_date.desc())
            )
            result = await session.execute(query)
            notification = result.scalars().all()

        else:
            query = select(NotificationModel).where(NotificationModel.id == notification_id)
            result = await session.execute(query)
            notification = result.scalar_one_or_none()

    return notification


async def update_notification(user_id, notification_id: int, db: AsyncSession):
    async with db as session:
        if notification_id is None:
            query = select(NotificationModel).where(
                NotificationModel.user_id == user_id
            )
            result = await session.execute(query)
            notifications = result.scalars().all()

            for notification in notifications:
                if notification.visualized is False:
                    notification.visualized = True

            await session.commit()

            return notifications

        query = select(NotificationModel).where(NotificationModel.id == notification_id)
        result = await session.execute(query)
        notification: NotificationModel = result.scalar_one_or_none()

        if notification:
            notification.visualized = True
            await session.commit()

            return notification
