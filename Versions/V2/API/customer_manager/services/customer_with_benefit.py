from sqlmodel import select

from models.customer import CustomerModel
from models.benefit import BenefitModel

from services.customer_event import create_customer_event
# from services.request_event import finished_request_events
# from services.consumer import consume_customer_queue

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_customers_with_benefits(customers, db):
    creator_user = customers["creator_user"]

    async with db as session:
        # Adicionar a função que consome a fila aqui
        # background_tasks.add_task(consume_customer_queue, session)
        
        for obj in customers["data"]:
            customer: CustomerModel = CustomerModel.parse_obj(obj["customer"])
            benefit: BenefitModel = BenefitModel.parse_obj(obj["benefit"])

            benefit.status_description = "Aguardando inclus\u00E3o"
            benefit.status = "awaiting_inclusion"

            query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == customer.cpf)
            result_existing_customer = await session.execute(query_existing_customer)
            existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

            if not existing_customer:
                # Adiciona o novo cliente
                new_customer: CustomerModel = customer
                session.add(new_customer)
                await session.flush()
                
                customer_id = new_customer.id

                # Adiciona o novo benefício
                benefit.customer_id = customer_id
                new_benefit: BenefitModel = benefit
                session.add(new_benefit)
                
                nb = new_benefit.nb

                await session.commit()

                # Adiciona o novo evento
                await create_customer_event(db, creator_user, customer_id, nb, "customer", "register")

            elif not existing_customer.id:
                print("Column 'id' not found in existing customer.")

            else:
                query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
                result_existing_benefit = await session.execute(query_existing_benefit)
                existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

                if not existing_benefit:
                    # Adiciona o novo beneficio
                    benefit.customer_id = existing_customer.id
                    new_benefit: BenefitModel = benefit
                    session.add(new_benefit)

                    customer_id = existing_customer.id
                    nb = new_benefit.nb

                    await session.commit()

                    # Adiciona o novo evento
                    await create_customer_event(db, creator_user, customer_id, nb, "customer", "register")
                    
                else:
                    print(f"Benefit {benefit.nb} already exists for customer {existing_customer.cpf}")
        
    # FINALIZA O EVENTO DE REQUISIÇÃO
    # await finished_request_events(db, creator_user, "customers")