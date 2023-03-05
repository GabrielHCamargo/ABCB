import datetime

from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.ticket import TicketModel
from models.customer import CustomerModel
from models.benefit import BenefitModel

from services.customer_event import create_customer_event

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_ticket(ticket, db):
    creator_user = ticket["creator_user"]
    ticket: TicketModel = TicketModel.parse_obj(ticket["data"])  
    
    async with db as session:
        query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == ticket.cpf)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:

            ticket.customer_id = existing_customer.id
            ticket.status = "registered"

            session.add(ticket)

            await session.commit()

            query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == existing_customer.id)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.first()

            customer_id = existing_customer.id
            nb = existing_benefit[0].nb
            
            # Novo Evento
            await create_customer_event(db, creator_user, customer_id, nb, None, "register", requested=ticket.requested_event)

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
    creator_user = ticket["creator_user"]
    ticket_update: TicketModel = TicketModel.parse_obj(ticket["data"])

    async with db as session:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()

        if ticket:

            for field, value in ticket_update.dict(exclude_unset=True).items():
                setattr(ticket, field, value)

            await session.commit()

            customer_id = ticket.customer_id
            nb = ticket.nb
            
            # Novo Evento
            await create_customer_event(db, creator_user, customer_id, nb, None, ticket_update.status, requested=ticket_update.requested_event)

            return ticket

        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")


async def del_ticket(ticket_id, db):
    creator_user = "PEDIR PARA O GABRIEL ARRUMAR"
    
    async with db as session:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()
        

        if ticket:
            
            ticket.status = "authorized"

            await session.commit()

            customer_id = ticket.customer_id
            nb = ticket.nb
            
            # Novo Evento
            await create_customer_event(db, creator_user, customer_id, nb, None, ticket.status, requested=ticket.requested_event)

            return ticket
        
        else:
            raise HTTPException(detail="ticket not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # FINALIZA O EVENTO DE REQUISIÇÃO
        # await finished_request_events(db, creator_user, "customers")
