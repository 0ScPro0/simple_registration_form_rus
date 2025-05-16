from sqlalchemy import select, delete, update
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

async def orm_add_user(session: AsyncSession, data: dict):
    obj = User(
        username = data["username"],
        email = data["email"],
        password = data["password"]
    )
    session.add(obj)
    await session.commit()

async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()  # Получаем список объектов User
    return [user.__dict__ for user in users]  # Преобразуем в список словарей