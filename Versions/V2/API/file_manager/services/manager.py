import os
import secrets
import warnings

from typing import Dict
from typing import List

from fastapi import UploadFile

from core.configs import settings

from services.process_file import process_base
from services.process_file import process_return
from services.process_file import process_transfers
from services.process_file import process_document
from services.requests import customer_manager_customers
from services.requests import customer_manager_benefits
from services.requests import customer_manager_discounts
from services.requests import customer_manager_documents
from services.create_file import create_file

from sqlalchemy.ext.asyncio import AsyncSession


async def common_manager(file: UploadFile, file_type, user_id, db: AsyncSession): 
    # Ignora os warnings
    warnings.simplefilter("ignore")
     
    # Ler o conteúdo do arquivo
    contents = await file.read()

    token = secrets.token_hex(16)
    extension = os.path.splitext(file.filename)[-1]        
    filename = f"{file_type.upper()}_{token}{extension}"
    file_location = os.path.join(settings.UPLOAD_TMP_DIR, filename)
    file_path = f"{file_type}/{filename}"

    # Cria o arquivo temporário para processamento
    with open(file_location, "wb") as f:
        f.write(contents)
        f.close()

    # Opções de processamento disponíveis para tipos de arquivo específicos
    processing_options: Dict = {
        "base": process_base,
        "return": process_return,
        "transfer": process_transfers,
    }

    processed_data: List

    # Verifica se o tipo de arquivo é suportado
    if not file_type in processing_options:
        return False
    else:
        # Processa o arquivo com a função específica do tipo de arquivo
        processed_data = await processing_options[file_type](contents)

    # Opções de gerenciamento de clientes disponíveis para tipos de arquivo específicos
    request_options: Dict = {
        "base": customer_manager_customers,
        "return": customer_manager_benefits,
        "transfer": customer_manager_discounts,
    }

    # Verifica se o tipo de arquivo é suportado
    if not file_type in request_options:
        return False
    else:
        # Gerencia o cliente com a função específica do tipo de arquivo
        await request_options[file_type](processed_data, user_id)

    # Cria o arquivo na base de dados
    await create_file(contents, filename, file_location, file_path, file_type, user_id, db)

    # Remove o arquivo temporário
    try:
        os.remove(file_location)
    except:
        pass


async def document_manager(files: List[UploadFile], file_type, user_id, db: AsyncSession):
    processed_data = []
    
    for file in files:
        contents = await file.read()

        token = secrets.token_hex(16)
        extension = os.path.splitext(file.filename)[-1]        
        filename = f"{file_type.upper()}_{token}{extension}"
        file_location = os.path.join(settings.UPLOAD_TMP_DIR, filename)
        file_path = f"{file_type}/{filename}"

        # Cria o arquivo no disco temporário para que ele possa ser processado
        with open(file_location, "wb") as f:
            f.write(contents)
            f.close()

        # Processa o documento e adiciona o objeto processado a uma lista
        processed_obj = await process_document(file, contents, filename, file_location, file_path, file_type, user_id, db)
        processed_data.append(processed_obj)


        # Remove o arquivo temporário após processá-lo
        try:
            os.remove(file_location)
        except:
            pass

    # Gerencia os documentos processados pelo cliente
    await customer_manager_documents(processed_data, user_id)