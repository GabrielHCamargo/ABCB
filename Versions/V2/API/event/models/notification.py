from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class NotificationModel(SQLModel, table=True):
    __tablename__: str = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    message: str
    creation_date: Optional[datetime.date]
    status: str
    visualized: bool