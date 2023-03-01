from typing import Optional
from pydantic import validator

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class DiscountModel(SQLModel, table=True):
    __tablename__: str = "discounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    benefit_id: Optional[int] = Field(default=None, foreign_key="benefits.id")
    nb: str
    discount: str
    date: Optional[datetime.date]

    @validator("date", pre=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            year = value[2:]
            month = value[:2]
            iso_date_str = f"{year}-{month}-01"
            value = datetime.date.fromisoformat(iso_date_str)
        return value