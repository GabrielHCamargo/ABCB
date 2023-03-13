from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class CustomersEventsModel(SQLModel, table=True):
    __tablename__: str = "customers_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    nb: str
    manipulated_object: str
    event_ocurred: str
    event_description: str
    creation_date: Optional[datetime.date]