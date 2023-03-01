from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class StatusCodeModel(SQLModel, table=True):
    __tablename__: str = "status_codes"

    id: Optional[int] = Field(default=None, primary_key=True)
    operation_code: str
    result_code: str
    error_code: str
    code_description: str
    status: str