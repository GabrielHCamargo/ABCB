import json
from aio_pika import connect_robust, Message
from sqlalchemy.ext.asyncio import AsyncSession
from services.customer import create_customers_with_benefits
from core.configs import settings


async def connect_robust(url: str):
    return await connect_robust(url)


async def consume_customer_queue(session: AsyncSession):
    connection = await connect_robust(settings.RABBITMQ_URL)

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue('customers', durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body.decode())

                async with session() as db:
                    async with db.begin():
                        customer = await create_customers_with_benefits(db, payload)

                print(f"Created customer: {customer['name']} with benefits: {customer['benefits']}")

    await connection.close()
