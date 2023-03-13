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
            start_date = data["start_date"]
            if start_date == 0:
                start_date = None
            else:
                try:
                    start_date = datetime.date.fromisoformat(start_date)
                except ValueError:
                    start_date = None
            data["start_date"] = start_date
        super().__init__(**data)