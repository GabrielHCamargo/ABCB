from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.ticket import TicketModel

# from models.customer_event import CustomersEventsModel

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


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


async def read_tickets_by_customer(customer_id, db):
    async with db as session:
        query_tickets = select(TicketModel).where(TicketModel.customer_id == customer_id)
        result_tickets = await session.execute(query_tickets)
        tickets = result_tickets.scalars().all()
        
        if tickets:

            return tickets
        
        else:
            return []
    
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")