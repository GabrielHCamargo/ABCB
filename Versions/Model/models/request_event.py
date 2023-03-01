from typing import Optional

from fastapi import Request

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class RequestEventModel(SQLModel, table=True):
    __tablename__: str = "request_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint: str
    method: str
    creator_user: str
    creation_date: Optional[datetime.date]
    completion_date: Optional[datetime.date]
    status: str