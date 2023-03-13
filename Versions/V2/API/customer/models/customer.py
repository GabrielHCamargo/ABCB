import datetime
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class CustomerModel(SQLModel, table=True): 
    __tablename__: str = "customers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cpf: str = Field(unique=True)
    rg: Optional[str]
    birth: Optional[str]
    mother: Optional[str]
    address: Optional[str]
    neighborhood: Optional[str]
    cep: Optional[str]
    city: Optional[str]
    state: Optional[str]
    phone: Optional[str]
    entity: Optional[int]

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()

    def __init__(self, **data):
        if "cpf" in data:
            data["cpf"] = "{:0>11}".format(int(data["cpf"]))
        super().__init__(**data)