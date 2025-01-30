from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserAuth
from app.utils.security import get_password_hash
from app.storage.models.user import User


async def create_user(session: AsyncSession, user: UserAuth):
    hashed_password = get_password_hash(user.password)
    async with session:
        await session.execute(
            insert(User).values(
                login=user.login,
                password=hashed_password,
            )
        )
        await session.commit()


async def check_user_exists(session: AsyncSession, login: str):
    async with session:
        user = await session.execute(select(User).where(User.login == login).limit(1))
        user = user.scalars().first()
        return user


async def get_user_by_login(session: AsyncSession, login: str):
    async with session:
        user = await session.execute(select(User).where(User.login == login).limit(1))
        user = user.scalars().first()
        return user