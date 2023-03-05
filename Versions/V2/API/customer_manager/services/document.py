import datetime

from sqlmodel import select

from models.customer import CustomerModel
from models.document import DocumentModel
from models.benefit import BenefitModel

from models.document_request import DocumentRequestModel

from models.customer_event import CustomersEventsModel

from services.customer_event import customers_events
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_documents(documents, db):
    event_customer = await customers_events(db, "document", "register")
    creator_user = documents["creator_user"]

    async with db as session:
        
        for obj in documents["data"]:
            document: DocumentRequestModel = DocumentRequestModel.parse_obj(obj)

            query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == document.cpf)
            result_existing_customer = await session.execute(query_existing_customer)
            existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

            if existing_customer:
                new_document: DocumentModel = DocumentModel(customer_id=existing_customer.id, token=document.token, creator_user=creator_user, creation_date=datetime.date.today())
                
                session.add(new_document)

                query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == existing_customer.id)
                result_existing_benefit = await session.execute(query_existing_benefit)
                existing_benefit: BenefitModel = result_existing_benefit.first()
                
                # Adiciona o novo evento
                new_customer_event: CustomersEventsModel = CustomersEventsModel(
                    customer_id=existing_customer.id,
                    nb=existing_benefit[0].nb,
                    manipulated_object=event_customer.manipulated_object,
                    event_ocurred=event_customer.event_ocurred,
                    event_description=event_customer.event_description,
                    creator_user=creator_user,
                    creation_date=datetime.date.today()
                )
                session.add(new_customer_event)

        await session.commit()

    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "documents")