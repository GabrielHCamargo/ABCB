import datetime

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.customer import CustomerModel
from models.document import DocumentModel
from models.benefit import BenefitModel

from models.document_request import DocumentRequestModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_documents(documents, db: AsyncSession):
    user_id = documents["user_id"]

    async with db as session:
        
        for obj in documents["data"]:

            # Converte os dados do objeto em um modelo DocumentRequestModel
            document: DocumentRequestModel = DocumentRequestModel.parse_obj(obj)

            # Busca o cliente correspondente ao CPF do documento, se existir
            query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == document.cpf)
            result_existing_customer = await session.execute(query_existing_customer)
            existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

            if existing_customer:

                # Se já existir um cliente com o CPF, adiciona o novo documento ao cliente
                new_document: DocumentModel = DocumentModel(
                    customer_id=existing_customer.id,
                    user_id=user_id,
                    token=document.token, 
                    url=document.url,
                    creation_date=datetime.date.today(),
                )
                
                session.add(new_document)

                await session.commit() # commit as mudanças na base de dados

                # Busca o benefício associado ao cliente
                query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == existing_customer.id)
                result_existing_benefit = await session.execute(query_existing_benefit)
                existing_benefit: BenefitModel = result_existing_benefit.first()

                customer_id = existing_customer.id
                nb = existing_benefit[0].nb
                
                # Cria um novo evento para registrar o registro do documento
                await create_customer_event(db, user_id, customer_id, nb, "document", "register")