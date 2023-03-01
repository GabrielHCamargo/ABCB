from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile

from services.requests import file_manager
from services.requests import customer_manager


router: APIRouter = APIRouter()


@router.post("/{file_type}", status_code=status.HTTP_200_OK)
async def post_file(file_type: str, file: UploadFile):
    if file:
        file_bytes = await file.read()

        # Enviar para Processamento de Arquivo em Json
        processed_data = await file_manager(file_bytes)

        # Enviar dados para o Gerenciador de Clientes
        customer_response = await customer_manager(processed_data)

        return {"msg": [customer_response]}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    

