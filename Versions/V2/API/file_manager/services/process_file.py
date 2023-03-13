import os
import pandas as pd
import warnings
from io import BytesIO
from datetime import datetime
from datetime import time

from fastapi import UploadFile

from models.file import FileModel

from services.create_file import create_file




def get_item_dict(row, cols):
    item_dict = {}
    for col in cols:
        value = row[col]
        if pd.isna(value):  # Verifica se o valor é NaN
            value = None
        elif isinstance(value, datetime):  # Verifica se o valor é datetime
            value = value.strftime("%Y-%m-%d")
        elif isinstance(value, time):  # Verifica se o valor é time
            value = value.strftime("%H:%M:%S")
        elif value in (None, "null", "Null", "nulo", "Nulo"):  # Verifica se o valor é None, "null", "Null" ou "Nulo"
            value = None
        item_dict[col.lower()] = value
    return item_dict



async def process_base(contents):
    # Ignora os warnings
    warnings.simplefilter("ignore")

    # Lê o conteúdo do arquivo enviado e converte-o em um DataFrame do Pandas
    df = pd.read_excel(BytesIO(contents))

    # Define os nomes das colunas que serão usados como chave em cada objeto
    customer_cols = [
        "NOME", 
        "CPF", 
        "RG", 
        "DATA NASCIMENTO", 
        "MAE",
        "ENDERECO", 
        "BAIRRO", 
        "CEP", 
        "CIDADE", 
        "ESTADO", 
        "TELEFONE",
    ]

    benefit_cols = [
        "NB", 
        "DIB", 
        "ESPECIE",
        "SALARIO", 
        "BANCO", 
        "AGENCIA", 
        "CONTA",
    ]

    # Remove a primeira linha do DataFrame, que contém apenas informações de cabeçalho
    df = df.iloc[1:]

    # Inicializa a lista que irá armazenar cada objeto de cliente/benefício
    result = []

    for i, row in df.iterrows():
        
        # Cria um dicionário de informações de cliente para a linha atual
        customer_dict = get_item_dict(row, customer_cols)

        # Renomeia as chaves do dicionário de acordo com os nomes de campo esperados pelo sistema
        customer_dict = {
            "name": customer_dict.pop("nome"),
            "cpf": customer_dict.pop("cpf"),
            "rg": customer_dict.pop("rg"),
            "birth": customer_dict.pop("data nascimento"),
            "mother": customer_dict.pop("mae"),
            "address": customer_dict.pop("endereco"),
            "neighborhood": customer_dict.pop("bairro"),
            "cep": customer_dict.pop("cep"),
            "city": customer_dict.pop("cidade"),
            "state": customer_dict.pop("estado"),
            "phone": customer_dict.pop("telefone"),
        }

        # Cria um dicionário de informações de benefício para a linha atual
        benefit_dict = get_item_dict(row, benefit_cols)

        # Renomeia as chaves do dicionário de acordo com os nomes de campo esperados pelo sistema
        benefit_dict = {
            "nb": benefit_dict.pop("nb"), 
            "dib": benefit_dict.pop("dib"), 
            "specie": benefit_dict.pop("especie"),
            "salary": benefit_dict.pop("salario"), 
            "bank": benefit_dict.pop("banco"), 
            "agency": benefit_dict.pop("agencia"),
            "account": benefit_dict.pop("conta")
        }

        # Adiciona o objeto de cliente/benefício à lista de resultados
        result.append({"customer": customer_dict, "benefit": benefit_dict})
    
    contents = None

    return result


async def process_return(contents):
    # lê o conteúdo do arquivo e divide em linhas
    lines = contents.decode().split("\n")
    
    lines = lines[1:-1]  # descartar a primeira e a última linha

    # processa cada linha e armazena em um dicionário
    data = []
    for line in lines:
        nb = line[1:11].strip()
        operation = line[11]
        result = line[12]
        error = line[13:16]
        discount = line[16:21]
        start_date = line[21:29].strip()

        # cria um dicionário com as informações obtidas
        obj = {
            "nb": nb,
            "operation": operation,
            "result": result,
            "error": error,
            "discount": discount,
            "start_date": start_date,
        }
        data.append(obj)

    contents = None

    return data


async def process_transfers(contents):
    # lê o conteúdo do arquivo e divide em linhas
    lines = contents.decode().split("\n")

    lines = lines[1:-1]  # descartar a primeira e a última linha

    # processa cada linha e armazena em um dicionário
    data = []
    for line in lines:
        nb = line[1:11].strip()
        discount = line[21:26]
        date = line[11:17]
        
        # cria um dicionário com as informações obtidas
        obj = {
            "nb": nb,
            "discount": discount,
            "date": date,
        }
        data.append(obj)
    
    contents = None

    return data


async def process_document(file: UploadFile, contents, filename, file_location, file_path, file_type, user_id, db):

    # Chamando a função assíncrona create_file() para criar o arquivo e salvar no banco de dados.
    file_db: FileModel = await create_file(contents, filename, file_location, file_path, file_type, user_id, db)
    cpf, extension = os.path.splitext(file.filename)
    
    # Criando um objeto com informações específicas sobre o arquivo salvo no banco de dados
    obj = {
        "token": file_db.token,
        "cpf": cpf,
        "url": file_db.url,
    }

    contents = None
    
    return obj