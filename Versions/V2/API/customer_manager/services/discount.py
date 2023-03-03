from sqlmodel import select

from models.benefit import BenefitModel
from models.discount import DiscountModel

# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_discounts(discounts, db):
    creator_user = discounts["creator_user"]

    async with db as session:
        
        for obj in discounts["data"]:
            new_discount: DiscountModel = DiscountModel.parse_obj(obj)

            query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == new_discount.nb)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

            if existing_benefit:
                new_discount.benefit_id = existing_benefit.id
                
                session.add(new_discount)

        await session.commit()
    
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "discounts")