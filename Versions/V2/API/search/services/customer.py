from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel
from models.discount import DiscountModel
from models.document import DocumentModel

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
        query_customer = select(CustomerModel).where(CustomerModel.id == customer_id)
        result_customer = await session.execute(query_customer)
        customer = result_customer.scalar_one_or_none()

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
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "benefits")