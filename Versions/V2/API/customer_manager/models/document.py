from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class DocumentModel(SQLModel, table=True):
    __tablename__: str = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    token: str
    url: str
    creation_date: Optional[datetime.date]
