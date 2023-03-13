from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.benefit import BenefitModel

from models.benefit_request import BenefitRequestModel
from models.status_code import StatusCodeModel

from services.customer_event import create_customer_event
from services.status_codes import status_codes

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def update_benefits(benefits, db: AsyncSession):
    status_codes_list = await status_codes(db) # obtem uma lista de status_codes da base de dados
    user_id = benefits["user_id"] # obtém o id do usuário das informações de benefícios

    async with db as session:
        
        for obj in benefits["data"]:

            # converte um dicionário em um objeto BenefitRequestModel
            benefit: BenefitRequestModel = BenefitRequestModel.parse_obj(obj)

            # encontra o objeto status_code correspondente para a operação, resultado e erro da solicitação de benefício atual
            status_code: StatusCodeModel = next(
                (
                    code for code in status_codes_list if code.operation_code == benefit.operation and 
                    code.result_code == benefit.result and code.error_code == benefit.error
                ), 
                None
            )

            # procura na base de dados se há um benefício existente com o mesmo número de benefício (nb)
            query = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
            result = await session.execute(query)
            existing_benefit: BenefitModel = result.scalar_one_or_none()

            if existing_benefit:
                # atualiza as informações do benefício existente
                existing_benefit.discount = benefit.discount
                existing_benefit.start_date = benefit.start_date
                existing_benefit.status_description = status_code.code_description
                existing_benefit.status = status_code.status

                await session.commit() # commit as mudanças na base de dados

                customer_id = existing_benefit.customer_id
                nb = customer_id

                # cria um novo evento de cliente na base de dados
                await create_customer_event(db, user_id, customer_id, nb, None, None, inss_return=True, status_code=status_code)