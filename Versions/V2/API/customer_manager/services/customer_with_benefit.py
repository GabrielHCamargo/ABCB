from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.customer import CustomerModel
from models.benefit import BenefitModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_customers_with_benefits(customers, db: AsyncSession):
    # Extrai o id do usuário da entrada de dados
    user_id = customers["user_id"]

    async with db as session:
        
        for obj in customers["data"]:

            # Converte os dados do cliente e do benefício em objetos dos modelos correspondentes
            customer: CustomerModel = CustomerModel.parse_obj(obj["customer"])
            benefit: BenefitModel = BenefitModel.parse_obj(obj["benefit"])

            # Define o status do benefício como "Aguardando inclusão"
            benefit.status_description = "Aguardando inclus\u00E3o"
            benefit.status = "awaiting_inclusion"

            # Verifica se já existe um cliente com o mesmo CPF no banco de dados
            query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == customer.cpf)
            result_existing_customer = await session.execute(query_existing_customer)
            existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

            # Se não existe um cliente com o CPF fornecido, adiciona o novo cliente
            if not existing_customer:
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

                # Adiciona o novo evento "register" para o novo cliente
                await create_customer_event(db, user_id, customer_id, nb, "customer", "register")

            elif not existing_customer.id:
                print("Column 'id' not found in existing customer.")

            # Se já existe um cliente com o CPF fornecido, adiciona o novo benefício para esse cliente
            else:
                query_existing_benefit = select(BenefitModel).where(BenefitModel.nb == benefit.nb)
                result_existing_benefit = await session.execute(query_existing_benefit)
                existing_benefit: BenefitModel = result_existing_benefit.scalar_one_or_none()

                if not existing_benefit:
                    # Adiciona o novo benefício para o cliente existente
                    benefit.customer_id = existing_customer.id
                    new_benefit: BenefitModel = benefit
                    session.add(new_benefit)

                    customer_id = existing_customer.id
                    nb = new_benefit.nb

                    await session.commit()

                    # Adiciona o novo evento "register" para o cliente existente
                    await create_customer_event(db, user_id, customer_id, nb, "customer", "register")
                    
                else:
                    # Se já existe um benefício com o mesmo número e mesmo cliente, exibe uma mensagem de erro
                    print(f"Benefit {benefit.nb} already exists for customer CPF {existing_customer.cpf}")