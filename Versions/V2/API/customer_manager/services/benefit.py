from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.benefit import BenefitModel

from models.benefit_request import BenefitRequestModel

from services.customer_event import create_customer_event
from services.status_codes import status_codes
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_benefits(benefits, db):
    status_codes_list = await status_codes(db)
    creator_user = benefits["creator_user"]

    # criar dicionário que mapeia as tuplas (operation, result, error) para instâncias de StatusCodeModel
    # status_codes_dict = {(s.operation_code, s.result_code, s.error_code): s for s in status_codes_list}

    async with db as session:
        
        for obj in benefits["data"]:
            benefit: BenefitRequestModel = BenefitRequestModel.parse_obj(obj)

            # verificar se a tupla de valores do benefício está no dicionário de status_codes
            # status_code = status_codes_dict.get((benefit.operation, benefit.result, benefit.error))
            status_code: None
            for code in status_codes_list:
                if code.operation_code == benefit.operation and code.result_code == benefit.result and code.error_code == benefit.error:
                    status_code = code

            query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

            if existing_benefit:
                existing_benefit.discount = benefit.discount
                existing_benefit.start_date = benefit.start_date

                await session.commit()

                customer_id = existing_benefit.customer_id
                nb = customer_id

                # Novo evento
                await create_customer_event(db, creator_user, customer_id, nb, None, None, inss_return=True, status_code=status_code)
                

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

            customer_id = existing_benefit.customer_id
            nb = existing_benefit.nb
            
            # Novo evento
            await create_customer_event(db, creator_user, customer_id, nb, "benefit", "update")

            return existing_benefit

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "discounts")