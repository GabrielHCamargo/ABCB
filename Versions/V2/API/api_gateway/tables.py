from sqlmodel import SQLModel

from core.database import engine


async def tables() -> None:
    import models.__all__
    print("Criando as tabelas no banco de dados...")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(tables())