from sqlmodel import SQLModel


class DocumentRequestModel(SQLModel, table=False):
    token: str
    cpf: str