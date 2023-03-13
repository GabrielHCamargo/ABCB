from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class CustomerEventCodeModel(SQLModel, table=True):
    __tablename__: str = "customers_events_codes"

    id: Optional[int] = Field(default=None, primary_key=True)
    manipulated_object: str
    event_ocurred: str
    event_description: str