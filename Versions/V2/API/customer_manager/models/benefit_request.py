from typing import Optional

from sqlmodel import SQLModel

import datetime

class BenefitRequestModel(SQLModel, table=False):
    nb: str
    operation: str
    result: str
    error: str
    discount: str
    start_date: Optional[datetime.date]

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()

    def __init__(self, **data):
        if "start_date" in data:
            data["start_date"] = datetime.date.fromisoformat(data["start_date"])
        super().__init__(**data)