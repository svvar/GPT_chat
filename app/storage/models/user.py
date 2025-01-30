from sqlalchemy import Column, Integer, String, DateTime, func

from ..models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registration_date = Column(DateTime, nullable=False, server_default=func.now())

