from typing import Optional, List

from sqlmodel import SQLModel
from sqlmodel import Field

from models.customer import CustomerModel

import datetime


class DocumentModel(SQLModel, table=True):
    __tablename__: str = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    token: str
    creator_user: str
    creation_date: Optional[datetime.date]