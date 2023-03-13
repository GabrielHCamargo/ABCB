from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.benefit import BenefitModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_benefit(benefit_id, benefit, db):
    user_id = benefit["user_id"]

    async with db as session:
        # Faz o parsing dos dados do benefício recebidos na requisição para o modelo do banco de dados
        benefit_update: BenefitModel = BenefitModel.parse_obj(benefit["data"])

        # Busca o benefício existente no banco de dados pelo seu ID
        query_existing_benefit = select(BenefitModel).where(BenefitModel.id == benefit_id)
        result_existing_benefit = await session.execute(query_existing_benefit)
        existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

        # Se o benefício existir no banco de dados, atualiza seus campos com os valores recebidos na requisição
        if existing_benefit:
            for field, value in benefit_update.dict(exclude_unset=True).items():
                setattr(existing_benefit, field, value)

            # Salva as alterações no banco de dados
            await session.commit()

            customer_id = existing_benefit.customer_id
            nb = existing_benefit.nb
            
            # Cria um novo evento no histórico do cliente, informando a atualização do benefício
            await create_customer_event(db, user_id, customer_id, nb, "benefit", "update")

            return existing_benefit

        else:
            raise HTTPException(detail="benefit not found", status_code=status.HTTP_404_NOT_FOUND)