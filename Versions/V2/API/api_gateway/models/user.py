from typing import Optional, List

from sqlmodel import SQLModel
from sqlmodel import Field


class UserModel(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    login: str
    mail: str
    password: str
    user_type: str
    status: str