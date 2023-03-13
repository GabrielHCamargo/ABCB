from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class EventModel(SQLModel, table=True):
    __tablename__: str = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    manipulated_object: str
    event_ocurred: str
    event_description: str
    creation_date: Optional[datetime.date]
    completion_date: Optional[datetime.date]
    status: str
