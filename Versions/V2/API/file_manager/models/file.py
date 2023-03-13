from typing import Optional, List

from sqlmodel import SQLModel
from sqlmodel import Field

import datetime


class FileModel(SQLModel, table=True):
    __tablename__: str = "files"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    token: str
    file_type: str
    url: str
    creation_date: Optional[datetime.date]