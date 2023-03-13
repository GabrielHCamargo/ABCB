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
            query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == new_discount.nb)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

            # Se o benefício existe
            if existing_benefit:

                # Verifica se já existe um desconto para esse benefício nesse mês
                query_existing_discount = select(DiscountModel).where(
                    (DiscountModel.date == new_discount.date) &
                    (DiscountModel.nb == new_discount.nb)
                )
                result_existing_discount = await session.execute(query_existing_discount)
                existing_discount: BenefitModel = result_existing_discount.scalar_one_or_none()

                if not existing_discount:
                    # Se o desconto para esse mês não existir, vincula o desconto a ele
                    new_discount.benefit_id = existing_benefit.id
                    
                    session.add(new_discount)

                    await session.commit() # commit as mudanças na base de dados

                    # Cria um novo evento para registrar a transferência de desconto
                    customer_id = existing_benefit.customer_id
                    nb = existing_benefit.nb

                    # Adiciona evento
                    await create_customer_event(db, user_id, customer_id, nb, "inss_transfer", "discount")
                
                else:
                    # Se o desconto desse mÊs existir retorna uma mensagem
                    print(f"The Discount on the date {new_discount.date} already exists the Benefits {new_discount.nb}")