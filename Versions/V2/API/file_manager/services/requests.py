import httpx

from core.configs import settings


async def customer_manager_customers(processed_data, user_id):
    async with httpx.AsyncClient() as client:
        url = f"{settings.CUSTOMER_MANAGER_V1_URL}/customers/"
        json_data = {"user_id": user_id, "data": processed_data}
        await client.post(url, json=json_data, follow_redirects=True)
    

async def customer_manager_benefits(processed_data, user_id):
    async with httpx.AsyncClient() as client:
        url = f"{settings.CUSTOMER_MANAGER_V1_URL}/benefits/"
        json_data = {"user_id": user_id, "data": processed_data}
        await client.post(url, json=json_data, follow_redirects=True)
    

async def customer_manager_discounts(processed_data, user_id):
    async with httpx.AsyncClient() as client:
        url = f"{settings.CUSTOMER_MANAGER_V1_URL}/discounts/"
        json_data = {"user_id": user_id, "data": processed_data}
        await client.post(url, json=json_data, follow_redirects=True)
    

async def customer_manager_documents(processed_data, user_id):
    async with httpx.AsyncClient() as client:
        url = f"{settings.CUSTOMER_MANAGER_V1_URL}/documents/"
        json_data = {"user_id": user_id, "data": processed_data}
        await client.post(url, json=json_data, follow_redirects=True)