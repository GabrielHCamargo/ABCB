from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class BenefitModel(SQLModel, table=True):
    __tablename__: str = "benefits"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    nb: str = Field(unique=True)
    dib: Optional[datetime.date]
    specie: Optional[int]
    salary: Optional[str]
    bank: Optional[str]
    agency: Optional[str]
    account: Optional[str]
    discount: Optional[str]
    start_date: Optional[datetime.date]
    status_description: str
    status: str