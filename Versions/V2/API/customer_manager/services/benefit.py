import datetime

from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.benefit import BenefitModel

from models.customer_event import CustomersEventsModel

from models.benefit_request import BenefitRequestModel

from services.customer_event import customers_events
from services.status_codes import status_codes
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_benefits(benefits, db):
    inss_return = [await customers_events(db, "inss_return", status) for status in ["activated", "error", "canceled"]]

    status_codes_list = await status_codes(db)
    creator_user = benefits["creator_user"]

    # criar dicionário que mapeia as tuplas (operation, result, error) para instâncias de StatusCodeModel
    status_codes_dict = {(s.operation_code, s.result_code, s.error_code): s for s in status_codes_list}

    async with db as session:
        
        for obj in benefits["data"]:
            benefit: BenefitRequestModel = BenefitRequestModel.parse_obj(obj)

            # verificar se a tupla de valores do benefício está no dicionário de status_codes
            status_code = status_codes_dict.get((benefit.operation, benefit.result, benefit.error))

            query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

            if existing_benefit:
                existing_benefit.discount = benefit.discount
                existing_benefit.start_date = benefit.start_date
                existing_benefit.status_description = status_code.code_description
                existing_benefit.status = status_code.status

                # Novo evento
                inss_event = next((inss for inss in inss_return if inss.event_ocurred == status_code.status), None)

                if inss_event:
                    new_customer_event = CustomersEventsModel(
                        customer_id=existing_benefit.customer_id,
                        nb=existing_benefit.nb,
                        manipulated_object=inss_event.manipulated_object,
                        event_ocurred=inss_event.event_ocurred,
                        event_description=inss_event.event_description,
                        creator_user=creator_user,
                        creation_date=datetime.date.today()
                    )

                    session.add(new_customer_event)
                
                await session.commit()

    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "benefits")


async def update_benefit(benefit_id, benefit, db):
    creator_user = benefit["creator_user"]

    async with db as session:
        benefit_update: BenefitModel = BenefitModel.parse_obj(benefit["data"])

        query_existing_benefit = select(BenefitModel).where(BenefitModel.id == benefit_id)
        result_existing_benefit = await session.execute(query_existing_benefit)
        existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

        if existing_benefit:
            for field, value in benefit_update.dict(exclude_unset=True).items():
                setattr(existing_benefit, field, value)

            await session.commit()

            return existing_benefit

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "discounts")