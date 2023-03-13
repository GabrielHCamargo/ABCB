from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.ticket import TicketModel

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def read_ticket(ticket_id, db: AsyncSession):
    async with db as session:
        # Cria uma consulta para obter o ticket com base no ID do ticket
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()
        
        # Verifica se o ticket foi encontrado
        if ticket:
            # Se o ticket foi encontrado, retorna o objeto de ticket
            return ticket
        
        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)


async def read_tickets_by_customer(customer_id, db: AsyncSession):
    async with db as session:
        # Cria uma consulta para obter todos os tickets com base no ID do cliente
        query_tickets = select(TicketModel).where(TicketModel.customer_id == customer_id)
        result_tickets = await session.execute(query_tickets)
        tickets = result_tickets.scalars().all()
        
        # Verifica se foram encontrados tickets para o cliente
        if tickets:

            # Se houver tickets, retorna a lista de objetos de ticket
            return tickets
        
        else:
            return []