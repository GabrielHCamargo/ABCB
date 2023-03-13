from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_customer(customer_id, customer, db):
    user_id = customer["user_id"]

    async with db as session:
        # Faz o parsing dos dados do cliente recebidos na requisição para o modelo do banco de dados
        customer_update: CustomerModel = CustomerModel.parse_obj(customer["data"])

        # Busca o cliente existente no banco de dados com o ID fornecido
        query_existing_customer = select(CustomerModel).where(CustomerModel.id == customer_id)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:
            # Atualiza os campos do cliente existente com os valores fornecidos
            for field, value in customer_update.dict(exclude_unset=True).items():
                setattr(existing_customer, field, value)
            
            await session.commit()

            # Busca o benefício existente do cliente atualizado
            query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == customer_id)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.first()
            nb = existing_benefit[0].nb

            # Adiciona um novo evento ao histórico do cliente
            await create_customer_event(db, user_id, customer_id, nb, "customer", "update")

            return existing_customer

        else:
            raise HTTPException(detail="customer not found", status_code=status.HTTP_404_NOT_FOUND)
