from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.ticket import TicketModel
from models.customer import CustomerModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_ticket(ticket, db):
    user_id = ticket["user_id"]

    # Transforma dados do ticket em um objeto TicketModel
    ticket: TicketModel = TicketModel.parse_obj(ticket["data"])  
    
    async with db as session:
        # Verifica se o cliente já existe pelo CPF informado no ticket
        query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == ticket.cpf)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:
            # Se o cliente existir, preenche o id do cliente no ticket e define o status do ticket como "register"
            ticket.customer_id = existing_customer.id
            ticket.status = "register"

            # Adiciona o ticket ao banco de dados
            session.add(ticket)

            await session.commit()

            customer_id = existing_customer.id
            nb = ticket.nb
            
            # Adiciona um novo evento ao cliente
            await create_customer_event(db, user_id, customer_id, nb, None, "register", requested=ticket.requested_event)

            return ticket

        else:
            raise HTTPException(detail="customer not found", status_code=status.HTTP_404_NOT_FOUND)


async def update_ticket(ticket_id, ticket, db):
    user_id = ticket["user_id"]

    # Transforma dados do ticket em um objeto TicketModel
    ticket_update: TicketModel = TicketModel.parse_obj(ticket["data"])

    async with db as session:
        # Verifica se o ticket já existe pelo id informado no ticket
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()

        if ticket:
            # Atualiza os campos do ticket com os valores definidos no dicionário ticket_update.
            for field, value in ticket_update.dict(exclude_unset=True).items():
                setattr(ticket, field, value)

            await session.commit()

            customer_id = ticket.customer_id
            nb = ticket.nb

            # Cria um novo evento do cliente para registrar a atualização do ticket
            await create_customer_event(db, user_id, customer_id, nb, None, ticket.status, requested=ticket.requested_event)

            return ticket

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)