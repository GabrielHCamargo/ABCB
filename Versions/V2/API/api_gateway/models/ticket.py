from typing import Optional, List

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class TicketModel(SQLModel, table=True):
    __tablename__: str = "tickets"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    name: str
    cpf: str
    nb: str
    requested_event: str
    discounts: Optional[str]
    bank: Optional[str]
    agency: Optional[str]
    account: Optional[str]
    method_payment: Optional[str]
    pix_key: Optional[str]
    message: Optional[str]
    creation_date: Optional[datetime.date]
    status: str