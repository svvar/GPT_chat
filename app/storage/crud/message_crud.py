from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.models.message import MessageType, Message


async def save_message(session: AsyncSession, user_id: int, message: str, message_type: MessageType):
    async with session:
        await session.execute(
            insert(Message).values(
                user_id=user_id,
                text=message,
                type=message_type,
            )
        )
        await session.commit()


async def get_history(session: AsyncSession, user_id: int, limit: int = 20):
    async with session:
        messages = await session.execute(
            select(Message).where(Message.user_id == user_id).limit(limit)
        )
        messages = messages.scalars().all()
        return messages


async def clean_history(session: AsyncSession, user_id: int):
    async with session:
        await session.execute(
            delete(Message).where(Message.user_id == user_id)
        )
        await session.commit()