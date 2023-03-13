import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from models.file import FileModel
from models.user import UserModel

from services.encode_file import encode_file
from services.cdn import upload_cdn


async def create_file(contents, filename, file_location, file_path, file_type, user_id, db: AsyncSession):
    # Codifica o arquivo usando a função 'encode_file'
    hashed_token = await encode_file(contents, filename)

    # URL do CDN
    url = await upload_cdn(file_location, file_path)

    async with db as session:

        # Cria um objeto UserModel com o ID do usuário
        user: UserModel = UserModel(id=user_id)

        # Cria um objeto FileModel com os dados do arquivo
        file_db: FileModel = FileModel(
            user_id=user.id,
            token=hashed_token,
            file_type=file_type,
            url=url,
            creation_date=datetime.date.today(),
        )

        # Adiciona o objeto FileModel à sessão do banco de dados
        session.add(file_db)
        await session.commit()
        
    if file_type == "document":
        return file_db