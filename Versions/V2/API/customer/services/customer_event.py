import datetime

from typing import List

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.customer_event_code import CustomerEventCodeModel
from models.customer_event import CustomersEventsModel
from models.user import UserModel


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_customer_event(
    db: AsyncSession, user_id, customer_id, nb, object, event, 
    requested=None, inss_return=None, status_code=None,
):
    
    # Cria uma instância do modelo UserModel com o ID do usuário
    user: UserModel = UserModel(id=user_id)

    # Se houver um retorno do INSS, cria eventos para os status "ativado", "erro" e "cancelado"
    if inss_return:
        events = [
            await customers_events(db, "inss_return", status)
            for status in ["activated", "error", "canceled"]
        ]

        async with db as session:

            # Encontra o evento INSS correspondente ao status_code fornecido
            inss_event = next(
                (inss for inss in events if inss.event_ocurred == status_code.status),
                None,
            )

            # Se o evento INSS for encontrado, cria um novo evento para o cliente
            if inss_event:
                new_customer_event = CustomersEventsModel(
                    customer_id=customer_id,
                    user_id=user.id,
                    nb=nb,
                    manipulated_object=inss_event.manipulated_object,
                    event_ocurred=inss_event.event_ocurred,
                    event_description=inss_event.event_description,
                    creation_date=datetime.date.today(),
                )

                # Adiciona o novo evento à sessão do banco de dados e faz o commit
                session.add(new_customer_event)
                await session.commit()

        # Retorna True se o evento foi criado com sucesso
        return True

    # Se não houver retorno do INSS, cria um novo evento para o objeto e o evento fornecidos
    event = await customers_events(db, object, event, requested)

    async with db as session:
        # Cria um novo evento para o cliente com base no objeto e evento fornecidos
        new_customer_event = CustomersEventsModel(
            customer_id=customer_id,
            user_id=user.id,
            nb=nb,
            manipulated_object=event.manipulated_object,
            event_ocurred=event.event_ocurred,
            event_description=event.event_description,
            creation_date=datetime.date.today(),
        )

        # Adiciona o novo evento à sessão do banco de dados e faz o commit
        session.add(new_customer_event)
        await session.commit()

    # Retorna True se o evento foi criado com sucesso
    return True


async def customers_events(db: AsyncSession, object, event, requested=None):

    async with db as session:
        
        # Crie uma consulta de seleção para o modelo CustomerEventCodeModel
        query = select(CustomerEventCodeModel)
        result = await session.execute(query)
        customer_event_code: List = result.all()

        # Crie um dicionário para mapear os valores de "requested" para os valores de "object"
        requested_to_object = {
            "cancel": "ticket_cancel",
            "reserve": "ticket_reserve",
            "others": "ticket_others",
        }

        # Obtenha o valor de "object" correspondente ao valor de "requested"
        if requested in requested_to_object:
            object = requested_to_object[requested]

        # Pesquise o objeto correspondente e retorne-o se encontrado
        for customer_event in customer_event_code:
            if (
                customer_event[0].manipulated_object == object
                and customer_event[0].event_ocurred == event
            ):
                return customer_event[0]

        # Se nenhum objeto correspondente for encontrado, retorne None
        return None