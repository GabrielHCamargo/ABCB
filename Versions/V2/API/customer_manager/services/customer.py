import datetime

from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel
from models.discount import DiscountModel
from models.document import DocumentModel

from models.customer_event import CustomersEventsModel

from models.benefit_request import BenefitRequestModel
from models.document_request import DocumentRequestModel

from services.customer_event import customers_events
from services.status_codes import status_codes
from services.ticket import read_tickets_by_customer
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def read_customer(customer_id, db):
    async with db as session:
        query_customers = select(CustomerModel).where(CustomerModel.id == customer_id)
        result_customers = await session.execute(query_customers)
        customer = result_customers.scalar_one_or_none()

        if customer:
            # Consulta para obter o documento do cliente
            query_document = select(DocumentModel).where(DocumentModel.customer_id == customer_id)
            result_document = await session.execute(query_document)
            document = result_document.scalar_one_or_none()

            # Consulta para obter os descontos do cliente
            query_benefit = select(BenefitModel).where(BenefitModel.customer_id == customer_id)
            result_benefit = await session.execute(query_benefit)

            # Agrupar benefícios por cliente
            benefits_by_customer = {}
            for benefit in result_benefit.scalars().all():
                if benefit.customer_id not in benefits_by_customer:
                    benefits_by_customer[benefit.customer_id] = []
                benefits_by_customer[benefit.customer_id].append(benefit)

            # Consulta para obter os descontos dos benefícios do cliente
            discount_models = []
            for benefit in benefits_by_customer.get(customer.id, []):
                discount_models.append(DiscountModel(benefit_id=benefit.id))

            query_discount = select(DiscountModel).where(
                DiscountModel.benefit_id.in_([d.benefit_id for d in discount_models])
            )
            result_discount = await session.execute(query_discount)

            # Agrupar descontos por benefício
            discounts_by_benefit = {}
            for discount in result_discount.scalars().all():
                if discount.benefit_id not in discounts_by_benefit:
                    discounts_by_benefit[discount.benefit_id] = []
                discounts_by_benefit[discount.benefit_id].append(discount)

            # Adicionar os dados dos documentos e descontos na resposta
            customer_with_benefits = customer.dict()
            if document:
                customer_with_benefits["document"] = document.dict()
            benefits = benefits_by_customer.get(customer.id, [])
            benefits_dict = []
            for benefit in benefits:
                benefit_dict = benefit.dict()
                discount_models = [d for d in discount_models if d.benefit_id == benefit.id]
                discounts = discounts_by_benefit.get(benefit.id, [])
                discounts_dict = [d.dict() for d in discounts]
                benefit_dict["discounts"] = discounts_dict
                benefits_dict.append(benefit_dict)
            customer_with_benefits["benefits"] = benefits_dict

            # Obter os tickets do cliente
            tickets = await read_tickets_by_customer(customer_id, db)

            # Adicionar os tickets ao dicionário de retorno
            tickets_dict = [t.dict() for t in tickets]
            customer_with_benefits["tickets"] = tickets_dict

            return customer_with_benefits

        

async def create_customers_with_benefits(customers, db):
    event_customer = await customers_events(db, "customer", "register")
    event_benefit = await customers_events(db, "benefit", "register")
    creator_user = customers["creator_user"]

    async with db as session:
        # Adicionar a função que consome a fila aqui
        # background_tasks.add_task(consume_customer_queue, session)
        
        for obj in customers["data"]:
            customer: CustomerModel = CustomerModel.parse_obj(obj["customer"])
            benefit: BenefitModel = BenefitModel.parse_obj(obj["benefit"])


            query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == customer.cpf)
            result_existing_customer = await session.execute(query_existing_customer)
            existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

            if not existing_customer:
                # Adiciona o novo cliente
                new_customer: CustomerModel = CustomerModel(name=customer.name, cpf=customer.cpf, rg=customer.rg)
                session.add(new_customer)
                await session.flush()

                # Adiciona o novo benefício
                new_benefit: BenefitModel = BenefitModel(customer_id=new_customer.id, nb=benefit.nb, status_description=benefit.status_description, status=benefit.status)
                session.add(new_benefit)

                # Adiciona o novo evento
                new_customer_event: CustomersEventsModel = CustomersEventsModel(
                   customer_id=new_customer.id,
                   nb=new_benefit.nb,
                   manipulated_object=event_customer.manipulated_object,
                   event_ocurred=event_customer.event_ocurred,
                   event_description=event_customer.event_description,
                   creator_user=creator_user,
                   creation_date=datetime.date.today()
                )
                session.add(new_customer_event)
                await session.commit()

            elif not existing_customer.id:
                print("Column 'id' not found in existing customer.")

            else:
                query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
                result_existing_benefit = await session.execute(query_existing_benefit)
                existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

                if not existing_benefit:
                    # Adiciona o novo beneficio
                    new_benefit: BenefitModel = BenefitModel(customer_id=existing_customer.id, nb=benefit.nb, status_description=benefit.status_description, status=benefit.status)
                    session.add(new_benefit)

                    # Adiciona o novo evento
                    new_customer_event: CustomersEventsModel = CustomersEventsModel(
                        customer_id=existing_customer.id,
                        nb=new_benefit.nb,
                        manipulated_object=event_benefit.manipulated_object,
                        event_ocurred=event_benefit.event_ocurred,
                        event_description=event_benefit.event_description,
                        creator_user=creator_user,
                        creation_date=datetime.date.today()
                    )
                    session.add(new_customer_event)
                    await session.commit()
                else:
                    print(f"Benefit {benefit.nb} already exists for customer {existing_customer.cpf}")
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")


async def update_customers_benefits(benefits, db):
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


async def create_documents(documents, db):
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

        await session.commit()

    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "documents")
