from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.status_code import StatusCodeModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def status_codes(db: AsyncSession):
    async with db as session:
        # Seleciona todos os modelos StatusCodeModel
        query = select(StatusCodeModel)
        result = await session.execute(query)
        # Retorna uma lista com os resultados da consulta
        return [row[0] for row in result.all()]