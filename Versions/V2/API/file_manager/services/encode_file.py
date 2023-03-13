import jwt
import hashlib

from core.configs import settings


async def encode_file(contents, filename):
    # Decodifica o conteúdo do arquivo em uma string usando o codec 'latin-1'
    contents_str: str = contents.decode('latin-1')
    # Cria um dicionário com o nome do arquivo e seu conteúdo
    data = {'file_name': filename, 'contents': contents_str}
    # Codifica o dicionário como um token JWT usando uma chave de criptografia
    token = jwt.encode(data, settings.SECRET_DOCUMENT_ENCRYPTION_KEY, algorithm='HS256')

    # Gera o hash SHA-256 do token JWT e retorna-o como uma string hex
    hashed_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
    return hashed_token
