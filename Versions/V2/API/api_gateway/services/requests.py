import httpx

from core.configs import settings


async def file_manager(file):
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.FILE_MANAGER_URL, data=file)
        return response.json()
    

async def customer_manager(processed_data):
    endpoint = "/customer"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.CUSTOMER_MANAGER_URL + endpoint, json=processed_data)
        return response.json()