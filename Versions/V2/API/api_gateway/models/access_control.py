from typing import Optional, List

from sqlmodel import SQLModel
from sqlmodel import Field


class AccessControlModel(SQLModel, table=True):
    __tablename__: str = "access_control"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_type: str
    allowed_endpoint: str