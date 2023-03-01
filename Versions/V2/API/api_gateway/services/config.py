from models.status_code import StatusCodeModel
from models.customer_event_code import CustomerEventCodeModel

from core.configs import settings


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


import csv


async def create_configs_database(db):
    async with db as session:
        with open(settings.STATUS_CODES_CSV, newline='', encoding='utf-8') as status_codes_file:
            reader = csv.reader(status_codes_file)
            next(reader)
            for row in reader:
                status_code = StatusCodeModel(
                    operation_code=row[0],
                    result_code=row[1],
                    error_code=row[2],
                    code_description=row[3],
                    status=row[4]
                )
                session.add(status_code)
            await session.commit()
        with open(settings.CUSTOMERS_EVENTS_CODES_CSV, newline='', encoding='utf-8') as customers_events_codes_file:
            reader = csv.reader(customers_events_codes_file)
            next(reader)
            for row in reader:
                customers_events_codes = CustomerEventCodeModel(
                    manipulated_object=row[0],
                    event_ocurred=row[1],
                    event_description=row[2],
                )
                session.add(customers_events_codes)
            await session.commit()

