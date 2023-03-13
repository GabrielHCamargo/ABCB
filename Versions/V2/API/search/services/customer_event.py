from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from models.customer_event import CustomersEventsModel

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def read_customer_event_by_customer(customer_id, db: AsyncSession):
    async with db as session:
        # Cria uma consulta para obter eventos de clientes com base no ID do cliente
        query = select(CustomersEventsModel).where(CustomersEventsModel.customer_id == customer_id)
        result = await session.execute(query)
        customer_event = result.scalars().all()
        
        # Verifica se há eventos retornados pela consulta
        if customer_event:
            # Se houver eventos, retorna a lista de objetos de evento
            return customer_event
        
        else:
            return []