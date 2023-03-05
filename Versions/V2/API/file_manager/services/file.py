import pandas as pd
import warnings

from io import BytesIO


def get_item_dict(row, cols):
    item_dict = {}
    for col in cols:
        value = row[col]
        if pd.isna(value):  # Verifica se o valor é NaN
            value = None
        item_dict[col.lower()] = value
    return item_dict


async def process_base(file):
    warnings.simplefilter("ignore")

    content = await file.read()
    df = pd.read_excel(BytesIO(content))

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

    # Remove a primeira linha
    df = df.iloc[1:]

    result = []
    for i, row in df.iterrows():
        customer_dict = get_item_dict(row, customer_cols)

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

        benefit_dict = get_item_dict(row, benefit_cols)

        benefit_dict = {
            "nb": benefit_dict.pop("nb"), 
            "dib": benefit_dict.pop("dib"), 
            "specie": benefit_dict.pop("especie"),
            "salary": benefit_dict.pop("salario"), 
            "bank": benefit_dict.pop("banco"), 
            "agency": benefit_dict.pop("agencia"),
            "account": benefit_dict.pop("conta")
        }

        result.append({"customer": customer_dict, "benefit": benefit_dict})
    
    return result


async def process_return(file):
    contents = await file.read()
    lines = contents.decode().split("\n")  # dividir o arquivo em linhas
    lines = lines[1:-1]  # descartar a primeira e a última linha

    data = []
    for line in lines:
        nb = line[1:11].strip()
        operation = line[11]
        result = line[12]
        error = line[13:16]
        discount = line[16:21]
        start_date = line[21:29].strip()
        obj = {
            "nb": nb,
            "operation": operation,
            "result": result,
            "error": error,
            "discount": discount,
            "start_date": start_date,
        }
        data.append(obj)
    
    return data


async def process_transfers(file):
    contents = await file.read()
    lines = contents.decode().split("\n")  # dividir o arquivo em linhas
    lines = lines[1:-1]  # descartar a primeira e a última linha

    data = []
    for line in lines:
        nb = line[1:11].strip()
        discount = line[21:26]
        date = line[11:17]
        obj = {
            "nb": nb,
            "discount": discount,
            "date": date,
        }
        data.append(obj)
    
    return data