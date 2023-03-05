import datetime

from fastapi import status
from fastapi import HTTPException

from sqlmodel import select

from models.ticket import TicketModel
from models.customer import CustomerModel
from models.benefit import BenefitModel

from models.customer_event import CustomersEventsModel

from services.customer_event import customers_events

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


async def create_ticket(ticket, db):
    creator_user = ticket["creator_user"]
    ticket: TicketModel = TicketModel.parse_obj(ticket["data"])

    event_customer = await customers_events(db, None, "register", requested=ticket.requested_event)
    
    
    async with db as session:
        query_existing_customer = select(CustomerModel).where(CustomerModel.cpf == ticket.cpf)
        result_existing_customer = await session.execute(query_existing_customer)
        existing_customer: CustomerModel = result_existing_customer.scalar_one_or_none()

        if existing_customer:

            ticket.customer_id = existing_customer.id
            ticket.status = "registered"

            session.add(ticket)

            query_existing_benefit = select(BenefitModel).where(BenefitModel.customer_id == existing_customer.id)
            result_existing_benefit = await session.execute(query_existing_benefit)
            existing_benefit: BenefitModel = result_existing_benefit.first()
            
            # Novo Evento
            new_customer_event: CustomersEventsModel = CustomersEventsModel(
                customer_id=existing_customer.id,
                nb=existing_benefit[0].nb,
                manipulated_object=event_customer.manipulated_object,
                event_ocurred=event_customer.event_ocurred,
                event_description=event_customer.event_description,
                creator_user=creator_user,
                creation_date=datetime.date.today()
            )
            session.add(new_customer_event)

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
    creator_user = ticket["creator_user"]
    ticket_update: TicketModel = TicketModel.parse_obj(ticket["data"])

    event_customer = await customers_events(db, None, ticket_update.status, requested=ticket_update.requested_event)
    print(event_customer)

    async with db as session:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await session.execute(query)
        ticket: TicketModel = result.scalar_one_or_none()

        if ticket:

            for field, value in ticket_update.dict(exclude_unset=True).items():
                setattr(ticket, field, value)

            # Novo Evento
            new_customer_event: CustomersEventsModel = CustomersEventsModel(
                customer_id=ticket.customer_id,
                nb=ticket.nb,
                manipulated_object=event_customer.manipulated_object,
                event_ocurred=event_customer.event_ocurred,
                event_description=event_customer.event_description,
                creator_user=creator_user,
                creation_date=datetime.date.today()
            )
            session.add(new_customer_event)

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
