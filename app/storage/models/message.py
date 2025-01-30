import enum

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum

from ..models import Base


class MessageType(enum.Enum):
    ASSISTANT = 'assistant'
    USER = 'user'

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(Enum(MessageType), nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())



