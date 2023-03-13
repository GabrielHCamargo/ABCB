from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.benefit import BenefitModel
from models.discount import DiscountModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_discounts(discounts, db: AsyncSession):
    user_id = discounts["user_id"]

    async with db as session:
        
        for obj in discounts["data"]:

            # Converte os dados em um modelo DiscountModel
            new_discount: DiscountModel = DiscountModel.parse_obj(obj)

            # Verifica se já existe um benefício com o mesmo número do novo desconto
            query = select(BenefitModel).where(BenefitModel.nb == new_discount.nb)
            result = await session.execute(query)
            existing_benefit: BenefitModel = result.scalar_one_or_none()

            if existing_benefit:

                 # Se o benefício já existir, vincula o desconto a ele
                new_discount.benefit_id = existing_benefit.id
                
                session.add(new_discount)

                await session.commit() # commit as mudanças na base de dados

                # Cria um novo evento para registrar a transferência de desconto
                customer_id = existing_benefit.customer_id
                nb = existing_benefit.nb

                # Adiciona evento
                await create_customer_event(db, user_id, customer_id, nb, "inss_transfer", "discount")