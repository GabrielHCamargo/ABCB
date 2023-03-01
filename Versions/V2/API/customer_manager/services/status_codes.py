from typing import List

from sqlmodel import select

from models.status_code import StatusCodeModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


import datetime



async def status_codes(db):
    async with db as session:
        query_customer_status_code = select(StatusCodeModel)
        result_customer_status_code = await session.execute(query_customer_status_code)
        status_codes = [row[0] for row in result_customer_status_code.all()]
        return status_codes