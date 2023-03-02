import datetime

from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.ticket import TicketModel
from models.customer import CustomerModel

# from models.customer_event import CustomersEventsModel

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_ticket(ticket, db):
    async with db as session:
        ticket: TicketModel = TicketModel.parse_obj(ticket["data"])

        query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == ticket.cpf)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:

            ticket.customer_id = existing_customer.id
            ticket.status = "registered"

            session.add(ticket)
            await session.commit()

            return ticket

        else:
            raise HTTPException(detail="customer not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")


async def read_ticket(ticket_id, db):
    async with db as session:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()
        

        if ticket:

            return ticket
        
        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")


async def update_ticket(ticket_id, ticket, db):
    async with db as session:
        ticket_update: TicketModel = TicketModel.parse_obj(ticket["data"])

        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()

        if ticket:

            for field, value in ticket_update.dict(exclude_unset=True).items():
                setattr(ticket, field, value)

            await session.commit()

            return ticket

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")


async def del_ticket(ticket_id, db):
    async with db as session:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()
        

        if ticket:
            
            ticket.status = "finished"

            await session.commit()

            return ticket
        
        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")
