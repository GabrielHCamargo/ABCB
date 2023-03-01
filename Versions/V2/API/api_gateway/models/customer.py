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
